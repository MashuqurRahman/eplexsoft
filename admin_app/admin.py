from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import admin_dashboard_models

# Register your models here.
admin.site.register(admin_dashboard_models.SubSubCategoryDeliveryCharge)

@admin.register(admin_dashboard_models.SteadfastConsignment)
class SteadfastConsignmentAdmin(admin.ModelAdmin):
    list_display  = ('order', 'consignment_id', 'tracking_code', 'status', 'updated_at')
    list_filter   = ('status',)
    search_fields = ('consignment_id', 'tracking_code', 'order__order_no')
    readonly_fields = ('consignment_id', 'tracking_code', 'status', 'raw_response', 'created_at', 'updated_at')


class SteadfastConsignmentInline(admin.StackedInline):
    model  = admin_dashboard_models.SteadfastConsignment
    extra  = 0
    readonly_fields = ('consignment_id', 'tracking_code', 'status', 'raw_response')


@admin.register(admin_dashboard_models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('order_no', 'user', 'order_status', 'payment_status', 'total_payable', 'courier_action')
    inlines       = [SteadfastConsignmentInline]

    def courier_action(self, obj):
        send_url  = reverse('send_to_steadfast', args=[obj.id])
        track_url = reverse('track_order', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">📦 Send to Steadfast</a>&nbsp;'
            '<a class="button" href="{}">🔍 Track</a>',
            send_url, track_url
        )
    courier_action.short_description = "Steadfast"
    courier_action.allow_tags = True
