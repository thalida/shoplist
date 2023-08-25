import graphene
from django.db.models import F, Q
from django_filters import filters, FilterSet, OrderingFilter
from shop.models import (
  Product,
  ProductCategory,
  ProductUnit,
  Store,
  StoreCategory,
  StoreProduct,
  StoreSection,
)

class ProductFilter(FilterSet):
  class Meta:
    model = Product
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
      'current_stock': ['lt', 'gt', 'exact'],
      'target_quantity': ['lt', 'gt', 'exact'],
    }

  unit = filters.ModelMultipleChoiceFilter(
    field_name='unit',
    to_field_name='uid',
    queryset=ProductUnit.objects.all(),
  )

  categories = filters.ModelMultipleChoiceFilter(
    field_name='categories',
    to_field_name='uid',
    queryset=ProductCategory.objects.all(),
  )

  stores = filters.ModelMultipleChoiceFilter(
    field_name='stores',
    to_field_name='uid',
    queryset=Store.objects.all(),
  )

  to_buy = filters.BooleanFilter(
    method='filter_to_buy'
  )

  def filter_to_buy(self, queryset, name, value):
    if value:
      return queryset.filter(Q(current_stock__lt=F('target_quantity')) | Q(current_stock__isnull=True))

    return queryset

  order_by = OrderingFilter(
    fields=['name', 'current_stock', 'target_quantity']
  )


class ProductCategoryFilter(FilterSet):
  class Meta:
    model = ProductCategory
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
      'color': ['exact'],
    }

  order_by = OrderingFilter(
    fields=['name', 'color']
  )


class StoreFilter(FilterSet):
  class Meta:
    model = Store
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
    }

  categories = filters.ModelMultipleChoiceFilter(
      field_name='categories',
      to_field_name='uid',
      queryset=StoreCategory.objects.all(),
  )

  products = filters.ModelMultipleChoiceFilter(
      field_name='products',
      to_field_name='uid',
      queryset=Product.objects.all(),
  )

  order_by = OrderingFilter(
    fields=['name']
  )


class StoreCategoryFilter(FilterSet):
  class Meta:
    model = StoreCategory
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
      'color': ['exact'],
    }

  order_by = OrderingFilter(
    fields=['name', 'color']
  )

class StoreProductFilter(FilterSet):
  class Meta:
    model = StoreProduct
    fields = {
      'store': ['exact'],
      'product': ['exact'],
      'price': ['exact'],
      'section': ['exact'],
    }

  order_by = OrderingFilter(
    fields=['store', 'product', 'price', 'section', 'aisle']
  )

class StoreSectionFilter(FilterSet):
  class Meta:
    model = StoreSection
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
      'section_type': ['exact'],
    }

  order_by = OrderingFilter(
    fields=['name', 'section_type']
  )


class ProductUnitFilter(FilterSet):
  class Meta:
    model = ProductUnit
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
    }

  order_by = OrderingFilter(
    fields=['name']
  )
