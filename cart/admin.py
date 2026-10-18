from django.contrib import admin
from .models import Order, Item
from django.urls import path
from django.http import HttpResponse 
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "admin/cart/order/change_list.html"
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('top-purchaser/', self.admin_site.admin_view(self.top_purchaser_view), name='cart_order_top_purchaser'),
            path('top_purchaser_list/',self.admin_site.admin_view(self.top_purchaser_list),name='cart_order_top_purchaser_list')
        ]
        return custom_urls + urls

    def top_purchaser_view(self, request):
        top_purchaser = Item.objects.filter(order__user__is_staff=False, order__user__is_superuser=False).values('order__user__username').annotate(total_purchased=Sum('quantity')).order_by('-total_purchased').first() 
        return render(request, 'admin/cart/order/top_purchaser.html', {'top_purchaser': top_purchaser})

    def top_purchaser_list(self, request):
        limit = request.GET.get('limit','')
        users = (
            User.objects
            .filter(is_staff=False, is_superuser=False)
            .annotate(
                total_purchased = Coalesce(Sum('order__item__quantity'), 0)
            )
            .order_by('-total_purchased', 'username')
        )

        if limit.isdigit() and int(limit) > 0:
            users = users[:int(limit)]

        return render(request,
                      'admin/cart/order/top_purchaser_list.html',
                      {
                          'users':users,
                          'limit':limit
                      }
                      )

admin.site.register(Item)