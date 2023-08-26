import graphene
from datetime import datetime, timedelta, time
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
  Pantry,
  PantryProduct,
  Recipe,
  RecipeCategory,
  RecipeProduct,
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


class PantryFilter(FilterSet):
  class Meta:
    model = Pantry
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
    }

  products = filters.ModelMultipleChoiceFilter(
    field_name='products',
    to_field_name='uid',
    queryset=Product.objects.all(),
  )

  order_by = OrderingFilter(
    fields=['name']
  )


class PantryProductFilter(FilterSet):
  class Meta:
    model = PantryProduct
    fields = {
      'pantry': ['exact'],
      'product': ['exact'],
      'product__name': ['exact', 'icontains'],
      'quantity': ['exact', 'gte', 'lte'],
      'minimum_quantity': ['exact', 'gte', 'lte'],
      'unit': ['exact'],
      'notes': ['exact', 'icontains'],
    }


  expiration_date = filters.DateFilter(
    field_name='expiration_date',
    lookup_expr='exact',
  )

  expiration_date__before = filters.DateFilter(
    field_name='expiration_date',
    lookup_expr='lte',
  )

  expiration_date__after = filters.DateFilter(
    field_name='expiration_date',
    lookup_expr='gte',
  )

  restock = filters.BooleanFilter(
    method='filter_restock',
  )

  def filter_restock(self, queryset, name, value):
    if not value:
      return queryset

    today = datetime.now().date()

    return (
      queryset
        .annotate(
          threshold_quantity=F('minimum_quantity') * F('buy_threshold'),
          needs_more=F('quantity') <= F('threshold_quantity'),
          is_expired=Q(expiration_date__lte=today),
        )
        .filter(
          Q(needs_more=True) | Q(is_expired=True)
        )
    )

  order_by = OrderingFilter(
    fields=['pantry', 'product', 'quantity', 'minimum_quantity', 'expiration_date', 'unit']
  )


class RecipeFilter(FilterSet):
  class Meta:
    model = Recipe
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
      'description': ['exact', 'icontains'],
      'url': ['exact', 'icontains'],
      'is_planned': ['exact'],
      'is_favorite': ['exact'],
    }

  categories = filters.ModelMultipleChoiceFilter(
    field_name='categories',
    to_field_name='uid',
    queryset=RecipeCategory.objects.all(),
  )

  products = filters.ModelMultipleChoiceFilter(
    field_name='products',
    to_field_name='uid',
    queryset=Product.objects.all(),
  )

  order_by = OrderingFilter(
    fields=['name']
  )


class RecipeCategoryFilter(FilterSet):
  class Meta:
    model = RecipeCategory
    fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains'],
      'color': ['exact'],
    }

  order_by = OrderingFilter(
    fields=['name', 'color']
  )


class RecipeProductFilter(FilterSet):
  class Meta:
    model = RecipeProduct
    fields = {
      'recipe': ['exact'],
      'product': ['exact'],
      'quantity': ['exact', 'gte', 'lte'],
      'unit': ['exact'],
    }

  order_by = OrderingFilter(
    fields=['recipe', 'product', 'quantity', 'unit']
  )
