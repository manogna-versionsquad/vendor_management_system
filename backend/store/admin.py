from django.contrib import admin
from .models import Product,Tax,Category,Gallery,Specification,Size,Color,Cart,CartOrder,CartOrderItem,ProductFaq,Review,Wishlist,Notification,Coupon
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 0

class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 0
    
class SizeInline(admin.TabularInline):
    model = Size
    
    extra = 0
    
class ColorInline(admin.TabularInline):
    model = Color
    extra = 0

class CartOrderItemsInlineAdmin(admin.TabularInline):
    model = CartOrderItem

#class CouponUsersInlineAdmin(admin.TabularInline):
 #   model = CouponUsers

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','category','shipping_amount','stock_qty',"in_stock",'vendor','featured']
    list_editable = ['featured']
    list_filter = ['date']
    search_fields = ['title']
    inlines = [GalleryInline,SpecificationInline,SizeInline,ColorInline]

class CartAdmin(ImportExportModelAdmin):
    list_display = ['product', 'cart_id', 'qty', 'price', 'sub_total' , 'shipping_amount', 'service_fee', 'tax_fee', 'total', 'country', 'size', 'color', 'date']

class CartOrderAdmin(ImportExportModelAdmin):
    inlines = [CartOrderItemsInlineAdmin]
    search_fields = ['oid', 'full_name', 'email', 'mobile']
    list_editable = ['order_status', 'payment_status']
    list_filter = ['payment_status', 'order_status']
    list_display = ['oid', 'payment_status', 'order_status', 'sub_total', 'shipping_amount', 'tax_fee', 'service_fee' ,'total', 'saved' ,'date']

class CartOrderItemsAdmin(ImportExportModelAdmin):
    list_filter = ['delivery_couriers', 'applied_coupon']
    list_editable = ['date']
    list_display = ['order_id', 'vendor', 'product' ,'qty', 'price', 'sub_total', 'shipping_amount' , 'service_fee', 'tax_fee', 'total' , 'delivery_couriers', 'applied_coupon', 'date']

class ProductFaqAdmin(ImportExportModelAdmin):
    list_editable = [ 'active', 'answer']
    list_display = ['user', 'question', 'answer' ,'active']

class CouponAdmin(ImportExportModelAdmin):
    #inlines = [CouponUsersInlineAdmin]
    list_editable = ['code', 'active', ]
    list_display = ['vendor' ,'code', 'discount', 'active', 'date']

class NotificationAdmin(ImportExportModelAdmin):
    list_editable = ['seen']
    list_display = ['order', 'seen', 'user', 'vendor', 'date']

class ReviewAdmin(ImportExportModelAdmin):
    #list_editable = ['active']
    #list_editable = ['active']
    list_display = ['user', 'product']
    #, 'review', 'reply' ,'rating', 'active']

admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartOrder)
admin.site.register(CartOrderItem)
admin.site.register(ProductFaq,ProductFaqAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Wishlist)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(Tax)