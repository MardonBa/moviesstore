from django.contrib import admin
from .models import Order, Item
from django.urls import path
from django.http import HttpResponse 
from django.db.models import Sum
from django.shortcuts import render

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('top-purchaser/', self.admin_site.admin_view(self.top_purchaser_view), name='cart_order_top_purchaser')
        ]
        return custom_urls + urls

    def top_purchaser_view(self, request):
        top_purchaser = Item.objects.filter(order__user__is_staff=False, order__user__is_superuser=False).values('order__user__username').annotate(total_purchased=Sum('quantity')).order_by('-total_purchased').first() 
        return render(request, 'admin/cart/order/top_purchaser.html', {'top_purchaser': top_purchaser})

admin.site.register(Item)