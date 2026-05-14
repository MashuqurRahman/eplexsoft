PRODUCT_STATUS_CHOICES = (
    ('', "--SELECT--"),
    ('active', "Active"),
    ('inactive', "Inactive"),
)

PAYMENT_STATUS_CHOICES = (
    ('', "--SELECT--"),
    ('pending', 'Pending'), 
    ('paid', 'Paid')
)

ORDER_STATUS_CHOICES = (
    ('', "--SELECT--"),
    ('pending', 'Pending'), 
    ('confirmed', 'Confirmed'), 
    ('shipped', 'Shipped'), 
    ('delivered', 'Delivered'), 
    ('cancelled', 'Cancelled'), 
    ('returned', 'Returned')
)

DELIVERY_DISCOUNT_TYPE_CHOICES = (
    ('', "--SELECT--"),
    ('delivery', "Delivery"),
    ('product', "Product"),
)

DELIVERY_LOCATION_CHOICES = (
    ('', "--SELECT--"),
    ('inside_dhaka', "Inside Dhaka"),
    ('outside_dhaka', "Outside Dhaka"),
)

PRODUCT_APPROVAL =(
    ("approved", "Approved"),
    ("not_approved", "Not Approved"),
)

BUSINESS_SETTING_CHOICES = (
    ('', "--SELECT--"),
    ('terms_and_conditions', "Terms & Conditions"),
    ('privacy_and_policy', "Privacy Policy"),
    ('return_refund', "Return & Refund Policy"),
    ('warranty', "Warranty Policy"),
    ('emi', "EMI Policy"),
)

STEADFAST_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('in_review', 'In Review'),
    ('hold', 'Hold'),
    ('delivered_approval_pending', 'Delivered Approval Pending'),
    ('partial_delivered_approval_pending', 'Partial Delivered Approval Pending'),
    ('cancelled_approval_pending', 'Cancelled Approval Pending'),
    ('unknown_approval_pending', 'Unknown Approval Pending'),
    ('delivered', 'Delivered'),
    ('partial_delivered', 'Partial Delivered'),
    ('cancelled', 'Cancelled'),
    ('unknown', 'Unknown'),
)

PATHAO_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('pickup_requested', 'Pickup Requested'),
    ('picked_up', 'Picked Up'),
    ('in_transit', 'In Transit'),
    ('out_for_delivery', 'Out for Delivery'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
    ('returned', 'Returned'),
    ('hold', 'Hold'),
)

REDX_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('picked_up', 'Picked Up'),
    ('in_transit', 'In Transit'),
    ('out_for_delivery', 'Out for Delivery'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
    ('returned', 'Returned'),
    ('hold', 'Hold'),
)

COLUMN_CHOICES = (
    ('', "--SELECT--"),
    ('1', "1"),
    ('2', "2"),
    ('3', "3"),
    ('4', "4"),
)