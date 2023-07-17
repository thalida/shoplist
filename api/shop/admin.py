from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Product,
    ProductCategory,
    ProductUnit,

    Store,
    StoreCategory,
    StoreSection,
    StoreProduct,

    List,
    ListCategory,
    ListProduct,
)

@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    """
    ProductCategory admin
    """
    list_display = ('name', 'color')
    list_editable = ('color',)


@admin.register(ProductUnit)
class ProductUnitAdmin(ModelAdmin):
    """
    ProductUnit admin
    """
    pass


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Product admin
    """
    list_display = ('name', 'categories_list', 'stores_list', 'lists_list')

    def categories_list(self, obj):
        """
        Return categories list
        """
        return ', '.join([category.name for category in obj.categories.all()])

    def stores_list(self, obj):
        """
        Return stores list
        """
        return ', '.join([store.name for store in obj.stores.all()])

    def lists_list(self, obj):
        """
        Return lists list
        """
        return ', '.join([list_.name for list_ in obj.lists.all()])


class StoreProductInline(TabularInline):
    """
    StoreProduct inline
    """
    model = StoreProduct
    extra = 0

class StoreSectionInline(TabularInline):
    """
    StoreSection inline
    """
    model = StoreSection
    extra = 0


@admin.register(StoreCategory)
class StoreCategoryAdmin(ModelAdmin):
    """
    StoreCategory admin
    """
    pass


@admin.register(StoreSection)
class StoreSectionAdmin(ModelAdmin):
    """
    StoreSection admin
    """
    list_display = ('name', 'section_type', 'store')
    list_filter = ('section_type', 'store')


@admin.register(Store)
class StoreAdmin(ModelAdmin):
    """
    Store admin
    """
    inlines = [
        StoreSectionInline,
        StoreProductInline,
    ]


class ListProductInline(TabularInline):
    """
    ListProduct inline
    """
    model = ListProduct
    extra = 0


@admin.register(ListCategory)
class ListCategoryAdmin(ModelAdmin):
    """
    ListCategory admin
    """
    pass

@admin.register(List)
class ListAdmin(ModelAdmin):
    """
    List admin
    """

    inlines = [
        ListProductInline,
    ]
