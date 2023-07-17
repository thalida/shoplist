import graphene
from django_filters import filters, FilterSet, OrderingFilter
from shop.models import (
  Product,
  ProductCategory,
  ProductUnit,
  Store,
  StoreCategory,
  StoreProduct,
  StoreSection,
  List,
  ListCategory,
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
      field_name='categories',
      to_field_name='uid',
      queryset=ProductCategory.objects.all(),
  )

  stores = filters.ModelMultipleChoiceFilter(
      field_name='stores',
      to_field_name='uid',
      queryset=Store.objects.all(),
  )

  lists = filters.ModelMultipleChoiceFilter(
      field_name='lists',
      to_field_name='uid',
      queryset=List.objects.all(),
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
      field_name='categories',
      to_field_name='uid',
      queryset=ListCategory.objects.all(),
  )

  products = filters.ModelMultipleChoiceFilter(
      field_name='products',
      to_field_name='uid',
      queryset=Product.objects.all(),
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
