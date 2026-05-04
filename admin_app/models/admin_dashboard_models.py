from django.db import models
import math
from django.db.models import Avg, Count, Sum
from django.core.validators import MinValueValidator
from decimal import Decimal
from accounts_app.models import User
from client_app.models import client_models
from ..views import global_function
from .choices import BUSINESS_SETTING_CHOICES, PRODUCT_STATUS_CHOICES, PAYMENT_STATUS_CHOICES, ORDER_STATUS_CHOICES, DELIVERY_DISCOUNT_TYPE_CHOICES, DELIVERY_LOCATION_CHOICES
from .choices import PRODUCT_STATUS_CHOICES, PAYMENT_STATUS_CHOICES, ORDER_STATUS_CHOICES, DELIVERY_DISCOUNT_TYPE_CHOICES, DELIVERY_LOCATION_CHOICES, PRODUCT_APPROVAL, STEADFAST_STATUS_CHOICES, PATHAO_STATUS_CHOICES, REDX_STATUS_CHOICES
from django.utils import timezone
from django.db.models import BooleanField, Case, When, Value
from django.db.models.functions import Now
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.utils import timezone
from django.utils.timezone import is_aware, make_aware
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


campaign_type_choices =(
    ('campaign', 'Campaign'),
    ('flash_sale', 'Flash Sale')
)


class Categories(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='categories/',blank=True,null=True)
    def __str__(self):
        return self.name
    
class SubCategories(models.Model):
    categories = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name='sub_categories')
    sub_cat_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='sub_categories/',blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sub_cat_name}"
    
class SubSubCategories(models.Model):
    sub_categories = models.ForeignKey(SubCategories, on_delete=models.PROTECT, related_name='sub_sub_categories')
    sub_sub_cat_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sub_sub_categories/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_sub_cat_name
    
class Brand(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Size(models.Model):
    value = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.value

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approval='approved', is_active=True)
    
class Product(models.Model):
    categories = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name='product_categories')
    sub_categories = models.ForeignKey(SubCategories, on_delete=models.PROTECT, related_name='product_sub_categories')
    sub_sub_categories = models.ForeignKey(SubSubCategories, on_delete=models.PROTECT, related_name='product_sub_sub_categories')
    delivery_discount = models.ForeignKey('DeliveryDiscount', on_delete=models.PROTECT, related_name='product_delivery_discount', blank=True, null=True)
    product_name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    moq= models.PositiveIntegerField(default=1)
    vat_tax_amount = models.FloatField(default=0, validators=[MinValueValidator(Decimal('0'))])
    gst_amount = models.FloatField(default=0, validators=[MinValueValidator(Decimal('0'))])
    approval = models.CharField(max_length=150, choices=PRODUCT_APPROVAL, default="approved", blank = True, null=True)
    is_applicable = models.BooleanField(default=False)
    is_popular=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_best_deal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_product_attribute  = models.OneToOneField("ProductAttribute", on_delete=models.SET_NULL, related_name='product_ui_representator', blank=True, null=True)

    objects = ActiveManager()
    all_objects = models.Manager()
    
    @property
    def product_stock_status(self):
        product_attributes = ProductAttribute.objects.filter(product = self )
        flag = False
        stock_qty = 0
        initial_stock = 0
        for attribute in product_attributes:
            if attribute.attribute_stock_status["status"]:
                flag = True
                stock_qty += attribute.attribute_stock_status["remaining_stock"]
                initial_stock += attribute.attribute_stock_status["initial_stock"]
        
        return {'flag':flag, 'stock_qty': stock_qty, 'initial_stock': initial_stock}
    
    @property
    def total_sold_count(self):
        stock_status = self.product_stock_status
        initial_stock = stock_status['initial_stock']

        sold_qty = initial_stock - self.product_stock_status['stock_qty'] + self.fake_sold_count
        
        return {'sold_qty': sold_qty }
            
    @property
    def fake_sold_count(self):
        sold_count = 0
        try:
            sold = ProductVarient.objects.get(product=self).sold_count
            if sold:
                sold_count = sold
            else:
                sold_count = 0
        except:
            sold_count = 0
        return sold_count


    @property
    def reviews_calculation(self):
        reviews = client_models.ReviewRating.objects.filter(product=self)
        total_reviews = reviews.count()
        average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0   

        rounded = round(average_rating * 2) / 2  
        full_stars = int(rounded)
        half_star = 1 if rounded - full_stars == 0.5 else 0
        empty_stars = 5 - full_stars - half_star

        star_counts = reviews.values('rating').annotate(count=Count('rating'))
        rating_data = {i:0 for i in range(1,6)}

        for item in star_counts:
            rating_data[int(item['rating'])] = item['count']

        rating_percent = {key: (value/total_reviews)*100 if total_reviews > 0 else 0 for key, value in rating_data.items()}

        return {
            'average_rating': average_rating,
            'total_reviews': total_reviews,
            'rating_data': rating_data,
            'rating_percent': rating_percent,
            'total_percent': (average_rating / 5) * 100,
            "full_stars": range(full_stars),
            "half_star": half_star,
            "empty_stars": range(empty_stars),
        }
        
        
    
    def __str__(self):
        return f'{self.sub_categories.sub_cat_name}/{self.product_name}'
    
class ProductVarient(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_varient')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='product_brand', blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='product_varient_unit')
    sku = models.CharField(max_length=100, unique=True,blank=True, null=True)
    # status = models.CharField(max_length=20, choices=PRODUCT_STATUS_CHOICES, default='active')
    sold_count = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0'))])
    cover_photo = models.ImageField(upload_to='product_cover_photo/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.product.product_name}"
    
    
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attribute')
    product_varient = models.ForeignKey(ProductVarient, on_delete=models.CASCADE, related_name='product_varient_attribute', blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='product_color', blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='product_size', blank=True, null=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))], blank=True, null=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))])
    final_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))], blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    is_cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_final_price(self):
        base = float(self.discount_price) if self.discount_price else float(self.regular_price)

        flash_sales = FlashSell.objects.filter(
            product=self.product,
            side_slider__isnull=False
        )

        flash_discount = 0
        if flash_sales.exists():
            item = flash_sales.first()
            if item.is_percentage:
                flash_discount = base * float(item.discount_amount / 100)
            else:
                flash_discount = float(item.discount_amount)

        return round(base - flash_discount, 2)

    def save(self, *args, **kwargs):
        self.final_price = self.calculate_final_price()
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.is_cover:
            Product.objects.filter(pk=self.product_id).update(
                cover_product_attribute=self
            )

            ProductAttribute.objects.filter(
                product=self.product,
                is_cover=True
            ).exclude(id=self.id).update(is_cover=False)
    
    @property
    def attribute_stock_status(self):
        ordered_quantity = OrderItem.objects.filter(product_attribute = self ).exclude(order__order_status = "cancelled" ).aggregate(qty = Sum("quantity"))
        
        ordered_quantity = ordered_quantity["qty"] or 0
        remaining_stock = self.stock - ordered_quantity
        
        if remaining_stock < self.product.moq:
            status = False
        else:
            status = True
            
        context = {
            'remaining_stock':remaining_stock,
            'status':status,
            'ordered_quantity': ordered_quantity,
            'initial_stock': self.stock
        }
        return context
        
    

   

    
    
    @property
    def weight_in_kg(self):
        return self.weight / 1000
    

    @property
    def product_price_after_regular_discount(self):
        return self.discount_price if self.discount_price else self.regular_price
    
    @property
    def product_final_price(self):
        product_price_after_regular_discount = self.product_price_after_regular_discount
        flash_sale_discount =  self.flash_sale_price_after_discount['discount_price']

        final_price = float(product_price_after_regular_discount) - float(flash_sale_discount)
        
    
        return  round(final_price, 2)
      
    
    @property
    def flash_sale_price_after_discount(self):
        flash_sales = FlashSell.objects.filter(product=self.product,  side_slider__in= SideSlider.objects.all())

        discount_percentage = 0
        if flash_sales:
            for item in flash_sales:
                if item.side_slider.campaign_type=="flash_sale":
                
                    if item.is_percentage:
                        discount_price = float(self.product_price_after_regular_discount)* float(item.discount_amount/100)
                        discount_percentage = item.discount_amount
                    else:
                        discount_price = float(item.discount_amount)
                        discount_percentage = (float(item.discount_amount)/float(self.regular_price))*100

                    return {
                        'discount_price': discount_price,
                        'discount_percentage': discount_percentage
                    }
                    
                else:
                    if item.is_percentage:
                        discount_price = float(self.product_price_after_regular_discount)* float(item.discount_amount/100)
                        discount_percentage = item.discount_amount
                    else:
                        discount_price = float(item.discount_amount)
                        discount_percentage = (float(item.discount_amount)/float(self.regular_price))*100

                    return {
                        'discount_price': discount_price,
                        'discount_percentage': discount_percentage
                        
                    }
        else:
            return {
                        'discount_price': 0,
                        'discount_percentage': 0
                        
                    }


    @property
    def final_discount(self):
        product_final_price = float(self.product_final_price)
        regular_price = float(self.regular_price)
        return{
            'total_discount': regular_price-product_final_price,
            'total_discount_percentage': round(((regular_price-product_final_price)/regular_price)*100,1)
        }
    

class ProductAttributeImage(models.Model):
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='product_attribute_image')
    image = models.ImageField(upload_to='product_attribute_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    


class AboutUs(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TermsCondition(models.Model):
    head = models.CharField(max_length=100, choices=BUSINESS_SETTING_CHOICES, blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PrivacyPolicy(models.Model):
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_products')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.email} - {self.product.product_name}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='carts')
    session_key = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey('CouponManagement', on_delete=models.CASCADE, related_name='cart_items_coupon', blank=True, null=True)
    delivery_location = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return f"Cart ({self.id})"

    # @property
    # def total_price(self):
    #     return sum(item.subtotal for item in self.items.all())
    
    @property
    def subtotal(self):
        cart = CartItem.objects.filter(cart=self)
        subtotal = 0
        for item in cart:
            subtotal += (item.quantity * item.product_attribute.regular_price)
        return subtotal
    
    @property
    def subtotal_after_discount(self):
        cart = CartItem.objects.filter(cart=self)
        subtotal = 0
        for item in cart:
            subtotal += (item.quantity * item.product_attribute.product_final_price)
        return subtotal
    
    @property
    def cart_discount(self):
        return float(self.subtotal) - float(self.subtotal_after_discount)
    

    @property
    def cart_product_kg_weight(self):
        cart_items = CartItem.objects.filter(cart_id=self)
        weight = 0
        for item in cart_items:
            weight += (item.product_attribute.weight_in_kg * item.quantity)

        
        return weight
    
    
    # @property
    # def cart_delivery_charge(self):
    #     discount_price = 0
    #     total_delivery_charge = 0
    #     cart_items = CartItem.objects.filter(cart_id=self)
    #     for item in cart_items:
    #         delivery_charges = DeliveryCharge.objects.filter(is_active=True)
    #         delivery_charge=[0]
    #         temp=[]
    #         for charge in delivery_charges:
    #             initial_charge = charge.initial_charge
    #             weight = self.cart_product_kg_weight
    #             if charge.initial_weight >= weight:
    #                 total_delivery_charge = initial_charge
    #             else:
    #                 total_delivery_charge = math.floor(weight - charge.initial_weight) * charge.increment_weight_per_unit
    #             temp.append({
    #                 'flat_delivery': False,
    #                 'discount_price': 0,
    #                 'total_delivery_charge': total_delivery_charge,
    #                 'location': charge.delivery_location
    #             })
    #         delivery_charge.append(temp)
    #         if item.product.delivery_discount:
    #             if item.product.delivery_discount.min_price <= self.subtotal_after_discount:
    #                 if item.product.delivery_discount.flat_delivery == -1:
    #                     discount_price = item.product.delivery_discount.discount_price
                        
    #                     return [1,{
    #                         'flat_delivery': False,
    #                         'discount_price': discount_price,
    #                         'total_delivery_charge': (total_delivery_charge - discount_price) if (total_delivery_charge - discount_price) >= 0 else 0,
    #                         'location': False
    #                     } ]
    #                 else:
    #                     return [1,{
    #                         'flat_delivery': True,
    #                         'discount_price': discount_price,
    #                         'total_delivery_charge': item.product.delivery_discount.flat_delivery,
    #                         'location': False
    #                     }]
    #         else:
    #             return delivery_charge


    @property
    def cart_delivery_charge(self):
        discount_price = 0
        total_delivery_charge = 0
        cart_items = CartItem.objects.filter(cart_id=self)

        if not cart_items.exists():
            return [0, []]

        for item in cart_items:
            delivery_charges = DeliveryCharge.objects.filter(is_active=True, delivery_location = self.delivery_location)
            temp = []

            for charge in delivery_charges:
                initial_charge = charge.initial_charge
                weight = self.cart_product_kg_weight


                if charge.initial_weight >= weight:
                    total_delivery_charge = initial_charge
                else:
                    total_delivery_charge = (
                        math.ceil(weight - charge.initial_weight)
                        * charge.increment_weight_per_unit
                    ) + initial_charge

                temp.append({
                    'flat_delivery': False,
                    'discount_price': 0,
                    'total_delivery_charge': total_delivery_charge,
                    'location': charge.delivery_location
                })

            if item.product.delivery_discount:
                if item.product.delivery_discount.min_price <= self.subtotal_after_discount:

                    if item.product.delivery_discount.flat_delivery == -1:
                        discount_price = item.product.delivery_discount.discount_price

                        # if item.product.delivery_discount.type == 'product':
                        #     delivery_charges = (self.subtotal_after_discount - discount_price) if (self.subtotal_after_discount - discount_price) >= 0 else 0
                        # else:
                        #     delivery_charges = (total_delivery_charge - discount_price) if (total_delivery_charge - discount_price) >= 0 else 0

                        return [1, {
                            'flat_delivery': False,
                            'discount_price': discount_price,
                            'total_delivery_charge': (total_delivery_charge - discount_price) if (total_delivery_charge - discount_price) >= 0 else 0,
                            'location': False
                        }]

                    else:
                        return [1, {
                            'flat_delivery': True,
                            'discount_price': discount_price,
                            'total_delivery_charge': item.product.delivery_discount.flat_delivery,
                            'location': False
                        }]

            return [0, temp]

        return [0, []]

            

    @property
    def vat_gst_amount(self):
        total_vat, total_gst, applicable_amount = 0, 0, 0
        cart_items = CartItem.objects.filter(cart=self)
        coupon_discount_price = global_function.coupon_discount_calculator(self, self.coupon)
        discount = Decimal(coupon_discount_price)
        
        # for item in cart_items:
        #     vat = Decimal(item.product.vat_tax_amount)
        #     gst = Decimal(item.product.gst_amount)
        #     is_percent = item.product.is_applicable
        #     is_product_coupon = (self.coupon and self.coupon == "product")

        #     # if is_percent:
        #     #     vat = ((float(item.cart_item_total_price) - (float(coupon_discount_price))) * float(vat)) / 100
        #     #     gst = ((float(item.cart_item_total_price) - (float(coupon_discount_price))) * float(gst)) / 100

        #     if is_percent:
        #         cart_item_total_price_after_coupon =  (float(item.cart_item_total_price) - float(coupon_discount_price)) if is_product_coupon else (float(item.cart_item_total_price))
        #         if cart_item_total_price_after_coupon <= 0:
        #             vat = 0
        #             gst = 0
        #         else:
        #             vat = (cart_item_total_price_after_coupon * float(vat)) / 100 
        #             gst = (cart_item_total_price_after_coupon * float(gst)) / 100
                    
        #     total_vat += float(vat)
        #     total_gst += float(gst)
            
        for item in cart_items:

            item_total = Decimal(item.cart_item_total_price)
            vat_rate = Decimal(item.product.vat_tax_amount)
            gst_rate = Decimal(item.product.gst_amount)
            is_percent = item.product.is_applicable

            base_amount = item_total
            # If product coupon, calculate item-level discount
            if self.coupon and self.coupon.type == "product":

                # if is_percent:
                #     print("item_total2", item_total) 
                #     discount = (item_total * Decimal(self.coupon.value)) / Decimal('100')
                #     print("discount", discount)
                # else:
                #      # fixed amount
                #     discount = Decimal(self.coupon.value)

                # base_amount = item_total - discount
                base_amount = item_total

            # Prevent negative
            base_amount = max(base_amount, Decimal('0'))
            if is_percent:
                vat = (base_amount * vat_rate) / Decimal('100')
                gst = (base_amount * gst_rate) / Decimal('100')
            else:
                if base_amount<=0:
                    vat = 0
                    gst = 0
                else:
                    # vat = vat_rate
                    # gst = gst_rate

                    vat = vat_rate * item.quantity
                    gst = gst_rate * item.quantity

            total_vat += vat
            total_gst += gst
            applicable_amount += item.cart_item_total_price

        return {
            'total_vat': float(total_vat),
            'total_gst': float(total_gst),
            'total_tax_amount': float(total_vat) + float(total_gst),
            'coupon_discount_price': float(coupon_discount_price)
        }
    

            
    @property
    def total_payable(self):
        coupon_discount_price = global_function.coupon_discount_calculator(self, self.coupon)

        delivery_data = self.cart_delivery_charge or [0, []]
        total_delivery_charge = 0 
        if self.delivery_location:
            if  delivery_data[0] == 0:
                for item in delivery_data[1]:
                    if item['location'] == self.delivery_location:
                        total_delivery_charge = item['total_delivery_charge']
                        break
            else:
                total_delivery_charge = delivery_data[1]['total_delivery_charge']
       

        total_after_coupon = float(self.subtotal_after_discount )+ float(total_delivery_charge) - float(coupon_discount_price)
        
        #

        return {
            'total_payable_amount': float(total_after_coupon) + float(self.vat_gst_amount['total_tax_amount']),
            'total_delivery_charge': total_delivery_charge
        }
    
    



    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cart_item')
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='cart_product_attribute')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(Decimal('1'))])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True) 
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product_attribute')

    def __str__(self):
        return f"{self.product.product_name} - {self.color} - {self.size}"
    
    @property
    def cart_item_total_price(self):
        return self.quantity * self.product_attribute.product_final_price
    
    
    # @property
    # def product_discout_price(self):
    #     return self.product_attribute.regular_price - self.product_attribute.discount_price
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_shipping_address',blank=True, null=True)
    full_name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)
    address_line = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)
    thana = models.CharField(max_length=100, blank=True, null=True)
    upozila = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.upozila}/{self.city}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order',blank=True, null=True)
    coupon = models.ForeignKey("CouponManagement", on_delete=models.CASCADE, related_name='coupon_of_order', blank=True, null=True)
    order_no = models.CharField(max_length=100, unique=True)
    total_payable= models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))], blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))], blank=True, null=True)
    sub_total_after_discount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))], blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))], blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=30, blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    shipping_method = models.CharField(max_length=20, choices=DELIVERY_LOCATION_CHOICES)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))], blank=True, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, related_name='user_order_shipping_address')
    vat = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))], blank=True, null=True)
    gst = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))], blank=True, null=True)
    coupon_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))], blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.order_no
    
 
    @property
    def order_total_price(self):
        total = Decimal('0.00')

        for item in OrderItem.objects.filter(order=self):
            total += (item.price * item.quantity) + item.tax_amount
        if self.discount:
            total -= self.discount

        return max(total, Decimal('0.007'))
    
    @property
    def order_wise_buying_price(self):
        order_item_obj = OrderItem.objects.filter(order=self)
        total = 0
        for item in order_item_obj:
            total += item.product_total_buying_price
        return total

    @property
    def order_wise_selling_price(self):
        order_item_obj = OrderItem.objects.filter(order=self)
        total = 0
        for item in order_item_obj:
            total += item.product_total_selling_price
        if self.coupon and self.coupon_price and self.coupon.type == "product":
            total -= self.coupon_price
        return total

    @property
    def order_wise_profit(self):
        return self.order_wise_selling_price - self.order_wise_buying_price
    
    @property
    def order_wise_products(self):
        order_obj =  OrderItem.objects.filter(order=self)
        product_list = [
            f"{item.product.product_name}({item.quantity})" for item in order_obj
        ]
        return ", ".join(product_list)
    
    @property
    def total_vat_gst_amount(self):
        return self.vat + self.gst
    

class SteadfastConsignment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='consignment')
    consignment_id = models.CharField(max_length=100, blank=True, null=True)
    tracking_code = models.CharField(max_length=100, blank=True, null=True)
    invoice = models.CharField(max_length=100, blank=True, null=True) 
    recipient_name = models.CharField(max_length=200, blank=True, null=True)
    recipient_phone = models.CharField(max_length=20, blank=True, null=True)
    recipient_address = models.TextField(blank=True, null=True)
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status  = models.CharField(max_length=100, choices=STEADFAST_STATUS_CHOICES, default='pending')
    raw_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consignment {self.consignment_id} | Order {self.order.order_no} | {self.status}"
    
class PathaoConsignment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='pathao_consignment')
    consignment_id = models.CharField(max_length=100, blank=True, null=True)  
    merchant_order_id = models.CharField(max_length=100, blank=True, null=True)
    recipient_name = models.CharField(max_length=200, blank=True, null=True)
    recipient_phone = models.CharField(max_length=20,  blank=True, null=True)
    recipient_address = models.TextField(blank=True, null=True)
    recipient_city = models.IntegerField(blank=True, null=True)    
    recipient_zone = models.IntegerField(blank=True, null=True)
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    delivery_type = models.IntegerField(blank=True, null=True)                # 48 = normal, 12 = on-demand
    item_type = models.IntegerField(blank=True, null=True)                # 2 = parcel
    status = models.CharField(max_length=100, choices=PATHAO_STATUS_CHOICES, default='pending')
    raw_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"Consignment {self.consignment_id} | Order {self.order.order_no} | {self.status}"
    
class RedxConsignment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='redx_consignment')
    tracking_id = models.CharField(max_length=100, blank=True, null=True)  
    merchant_invoice_id = models.CharField(max_length=100, blank=True, null=True) 
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    customer_phone = models.CharField(max_length=20,  blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)
    delivery_area = models.CharField(max_length=200, blank=True, null=True)  
    delivery_area_id = models.IntegerField(blank=True, null=True)    
    cash_collection_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    parcel_weight = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=REDX_STATUS_CHOICES, default='pending')
    raw_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"Consignment {self.tracking_id} | Order {self.order.order_no} | {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_order_item')
    product_variant = models.ForeignKey(ProductVarient, on_delete=models.CASCADE, related_name='product_varient_item', blank=True, null=True)
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='product_attribute_order_item' )
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1'))])
    quantity = models.PositiveIntegerField()
    sub_total = models.FloatField(blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.product}/{self.price}"
    
    def save(self, *args, **kwargs):
        if self.product_attribute:
            self.buying_price = self.product_attribute.buying_price
        super().save(*args, **kwargs)

    @property
    def product_total_buying_price(self):
        return self.buying_price * self.quantity

    @property
    def product_total_selling_price(self):
        return self.price * self.quantity
    


class SiteSetting(models.Model):
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='site/logo/')
    favicon = models.ImageField(upload_to='site/favicon/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    numeric_validator = RegexValidator(r'^\+?\d+$', 'Only numeric digits (start with optional +) are allowed.')
    phone = models.CharField(max_length=20, validators=[numeric_validator], blank=True, null=True)
    company_moto = models.CharField(max_length=255, blank=True, null=True)
    company_google_app = models.URLField(max_length=500, blank=True, null=True)
    company_apple_app = models.URLField(max_length=500, blank=True, null=True)
    facebook = models.URLField(max_length=500, blank=True, null=True)
    whatsapp = models.URLField(max_length=500, blank=True, null=True)
    youtube = models.URLField(max_length=500, blank=True, null=True)
    linkedin = models.URLField(max_length=500, blank=True, null=True)
    instagram = models.URLField(max_length=500, blank=True, null=True)
    tiktok = models.URLField(max_length=500, blank=True, null=True)
    xhandle = models.URLField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.company_name
    
class paymentMethodLogos(models.Model):
    logo = models.ImageField(upload_to='payment_method_logos/')



class SideSliderActiveQueryset(models.QuerySet):
    def with_is_active_calc(self):
        now = timezone.now()
        return self.annotate(
            is_active=Case(
                When(
                    start_date__lte=now,
                    end_date__gte=now,
                    start_date__isnull=False,
                    end_date__isnull=False,
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )
        )
    def active(self):
        # Return only active sliders
        return self.with_is_active_calc().filter(is_active=True)


class SideSliderActiveManager(models.Manager):
    def get_queryset(self):
        return SideSliderActiveQueryset(self.model, using=self._db).active()


class SideSlider(models.Model):
    campaign_name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='side_sliders/')
    # is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    campaign_type = models.CharField(max_length=150, choices=campaign_type_choices, default='flash_sale')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    all_objects = models.Manager()       
    objects =SideSliderActiveManager()

    # @property
    # def is_active_calculation(self):
    #     now = timezone.now()
    #     try:
    #         return self.start_date <= now <= self.end_date
    #     except:
    #         return False
        
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)


    def __str__(self):
        
        return f"{self.campaign_name}"
    
    @property
    def is_active_status(self):
        """
        Returns True if the current time is between start_date and end_date, including hours/minutes/seconds.
        Handles nulls and timezone correctly.
        """
        now = timezone.now()
       

        if not self.start_date or not self.end_date:
            return False

        start = self.start_date
        end = self.end_date

        # Make sure datetimes are aware
        if not is_aware(start):
            start = make_aware(start, timezone.get_current_timezone())
        if not is_aware(end):
            end = make_aware(end, timezone.get_current_timezone())

        return start <= now <= end
    
class Slider(models.Model):
    image = models.ImageField(upload_to='sliders/')
    name = models.CharField(max_length=100, unique=True)
    slider_url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.Product} ({status})"
    
class FlashSell(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='flash_sell_product', blank=True, null=True)
    side_slider = models.ForeignKey(SideSlider, on_delete=models.PROTECT, related_name='flash_sell_side_slider')
    slider = models.ForeignKey(Slider, on_delete=models.PROTECT, related_name='flash_sell_slider', blank=True, null=True)
    discount_amount = models.FloatField(validators=[MinValueValidator(Decimal('1'))])
    is_percentage = models.BooleanField(default=False)
    # start_date = models.DateTimeField()
    # end_date = models.DateTimeField()

    class Meta:
        unique_together = ('product', 'side_slider')


    def clean(self):
        super().clean()
        if not self.product or not self.side_slider:
            return

        now = timezone.now()

        conflict_exists = FlashSell.objects.filter(
            product=self.product,
            side_slider__start_date__lte=now,
            side_slider__end_date__gte=now,
        ).exclude(pk=self.pk).exists()

        if conflict_exists:
            raise ValidationError({
            'product': (
                f"({self.product.product_name}) "
                f"is already in another active campaign."
                f"Please Re Enter the Campaign"
            )
        })
        
    def save(self, *args, **kwargs):
        self.full_clean()  
        return super().save(*args, **kwargs)

    def __str__(self):
        if self.product:
            return f"{self.product.product_name} - {self.discount_amount}"
        return f"FlashSell {self.pk}"
    
    
class DeliveryCharge(models.Model):
    initial_charge = models.FloatField(blank=True, null=True, validators=[MinValueValidator(Decimal('1'))])
    initial_weight = models.FloatField(blank=True, null=True, validators=[MinValueValidator(Decimal('1'))])
    initial_unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='initial_unit_of_product', blank=True, null=True)
    increment_weight_per_unit = models.FloatField(blank=True, null=True, validators=[MinValueValidator(Decimal('1'))])
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='delivery_charge_unit', blank=True, null=True)
    delivery_location = models.CharField(max_length=20, choices=DELIVERY_LOCATION_CHOICES)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('delivery_location', 'is_active')
    
    def __str__(self):
        return f'Initial Charge: {self.initial_charge}/{self.increment_weight_per_unit}'
    
class DeliveryDiscount(models.Model):
    flat_delivery = models.FloatField(default=-1)
    discount_price = models.FloatField(blank=True, null=True, default=0, validators=[MinValueValidator(Decimal('0'))])
    min_price = models.FloatField(default=0, validators=[MinValueValidator(Decimal('0'))])
    type = models.CharField(max_length=20, blank=True, default='delivery')

    def __str__(self):
        if self.flat_delivery == -1:
            if self.discount_price is not None:
                return f'Delivery-{self.discount_price:.0f}'
            else:
                return f'Delivery-0'
        return f'Flat-{self.flat_delivery:.0f}'
    
class RecentlyViewedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=1)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.user} → {self.product} ({self.view_count})"


class CouponManagement(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=30, unique=True)
    value = models.FloatField(validators=[MinValueValidator(Decimal('1'))])
    type = models.CharField(max_length=20, choices=DELIVERY_DISCOUNT_TYPE_CHOICES)
    min_price = models.FloatField(default=0, validators=[MinValueValidator(Decimal('0'))])
    number_of_user = models.PositiveIntegerField()
    is_percent = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name}/{self.code}"
    
    @property
    def used_coupon(self):
        used_coupon = Order.objects.filter(coupon=self).count()
        return {
            'coupon_balance': self.number_of_user - used_coupon,
            'used_coupon': used_coupon
        }


class SubSubCategoryDeliveryCharge(models.Model):
    sub_sub_category = models.ForeignKey(SubSubCategories, on_delete=models.PROTECT, related_name='delivery_charge_sub_sub_category')
    delivery_charge = models.ForeignKey(DeliveryCharge, on_delete=models.PROTECT, related_name='delivery_charge_of_sub_sub_category')

    def __str__(self):
        return f"{self.sub_sub_category}/{self.delivery_charge.initial_charge}"


class ThemeSetting(models.Model):
    primary_color = models.CharField(max_length=20, default="#eb2e61")
    secondary_color = models.CharField(max_length=20, default="#fbd5df")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Theme Settings"

class ClientThemeSetting(models.Model):
    footer_color = models.CharField(max_length=20, default="#761731")
    notification_color = models.CharField(max_length=20, default="#EF4444")
    price_color = models.CharField(max_length=20, default="#EF4444")
    button_color = models.CharField(max_length=20, default="#EB2E61")
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Client Theme Settings"

class EmployeeCategories(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_of_category')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='category_of_employee')
    
    def __str__(self):
        return self.category.name


class Courier(models.Model):
    provider = models.CharField(max_length=20, default='steadfast', blank=True)
    api_key = models.CharField(max_length=250)
    secret_key = models.CharField(max_length=250)
    base_url = models.URLField(max_length=500)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status:
            Courier.objects.exclude(id=self.id).update(status=False)
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"API Key: {self.api_key}"
    
class PathaoCourier(models.Model):
    provider = models.CharField(max_length=20, default='pathao', blank=True)
    api_key = models.CharField(max_length=250)
    secret_key = models.CharField(max_length=250)
    base_url = models.URLField(max_length=500)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    store_id = models.IntegerField(null=True, blank=True)
    city_id  = models.IntegerField(null=True, blank=True)
    zone_id  = models.IntegerField(null=True, blank=True)
    area_id  = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"API Key: {self.api_key}"
    
class RedxCourier(models.Model):
    provider = models.CharField(max_length=20, default='redx', blank=True)
    base_url = models.URLField(max_length=500)
    api_key = models.CharField(max_length=250)
    pickup_store_id = models.CharField(max_length=100, blank=True)
    pickup_phone = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=False)
    is_sandbox = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"API Key: {self.api_key}"