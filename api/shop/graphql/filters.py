import graphene
from django_filters import filters, FilterSet, OrderingFilter
from shop.models import (
  Product,
  Store,
  List,
  StoreCategory,
  ListCategory,
  ProductCategory,
  ProductUnit,
  StoreProduct,
  ListProduct,
)

class ProductFilter(FilterSet):
  class Meta:
    model = Product
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
    }

  categories = filters.ModelMultipleChoiceFilter(
      field_name='categories__uid',
      to_field_name='uid',
      queryset=ProductCategory.objects.all(),
  )

  stores = filters.ModelMultipleChoiceFilter(
      field_name='stores__uid',
      to_field_name='uid',
      queryset=Store.objects.all(),
  )

  lists = filters.ModelMultipleChoiceFilter(
      field_name='lists__uid',
      to_field_name='list__uid',
      queryset=ListProduct.objects.all(),
  )

  order_by = OrderingFilter(
    fields=['name']
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


class ListFilter(FilterSet):
  class Meta:
    model = List
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
    }

  categories = filters.ModelMultipleChoiceFilter(
      field_name='categories__uid',
      to_field_name='uid',
      queryset=ListCategory.objects.all(),
  )

  products = filters.ModelMultipleChoiceFilter(
      field_name='products__uid',
      to_field_name='uid',
      queryset=ListProduct.objects.all(),
  )

  order_by = OrderingFilter(
    fields=['name']
  )


class ListProductFilter(FilterSet):
  class Meta:
    model = ListProduct
    fields = {
      'list': ['exact'],
      'product': ['exact'],
      'quantity_have': ['exact'],
      'quantity_needed': ['exact'],
      'unit': ['exact'],
    }

  order_by = OrderingFilter(
    fields=['list', 'product', 'quantity_have', 'quantity_needed', 'unit']
  )


class ListCategoryFilter(FilterSet):
  class Meta:
    model = ListCategory
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
      field_name='categories__uid',
      to_field_name='uid',
      queryset=StoreCategory.objects.all(),
  )

  products = filters.ModelMultipleChoiceFilter(
      field_name='products__uid',
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
      'aisle': ['exact'],
    }

  order_by = OrderingFilter(
    fields=['store', 'product', 'price', 'section', 'aisle']
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
