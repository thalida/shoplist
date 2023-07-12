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
      'stores': ['exact'],
      'lists': ['exact'],
    }

  category = filters.ModelMultipleChoiceFilter(
      field_name='category__uuid',
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
      to_field_name='uid',
      queryset=List.objects.all(),
  )

  order_by = OrderingFilter(
    fields=['name', 'category']
  )
