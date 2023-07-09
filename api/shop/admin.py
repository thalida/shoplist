from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from .models import Product, Store, StoreProduct, List, ListProduct

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Product admin
    """
    pass


class StoreProductInline(TabularInline):
    """
    StoreProduct inline
    """
    model = StoreProduct
    extra = 0

@admin.register(Store)
class StoreAdmin(ModelAdmin):
    """
    Store admin
    """
    inlines = [
        StoreProductInline,
    ]


class ListProductInline(TabularInline):
    """
    ListProduct inline
    """
    model = ListProduct
    extra = 0


@admin.register(List)
class ListAdmin(ModelAdmin):
    """
    List admin
    """

    inlines = [
        ListProductInline,
    ]
