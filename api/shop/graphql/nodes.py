import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

from api.graphql import ConnectionWithTotalCount
from api.permissions import IsAuthenticated
from shop.models import (
  Product,
  ProductCategory,
  ProductUnit,
  Store,
  StoreCategory,
  StoreSection,
  StoreSectionType,
  StoreProduct,
)
from shop.graphql.filters import (
  ProductFilter,
  ProductCategoryFilter,
  ProductUnitFilter,
  StoreFilter,
  StoreCategoryFilter,
  StoreProductFilter,
  StoreSectionFilter,
)

class ProductNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = Product
    fields = ['uid', 'name', 'current_stock', 'target_quantity', 'unit', 'categories', 'stores', 'created_at', 'updated_at']
    filterset_class = ProductFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount

  stores = DjangoFilterConnectionField(lambda: StoreProductNode, filterset_class=StoreProductFilter)

  def resolve_stores(self, info, **kwargs):
    return StoreProduct.objects.filter(product=self)


class ProductCategoryNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = ProductCategory
    fields = ['uid', 'name', 'color', 'created_at', 'updated_at']
    filterset_class = ProductCategoryFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class ProductUnitNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = ProductUnit
    fields = ['uid', 'name', 'abbreviation', 'created_at', 'updated_at']
    filterset_class = ProductUnitFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class StoreNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = Store
    fields = ['uid', 'name', 'categories', 'products', 'sections', 'created_at', 'updated_at']
    filterset_class = StoreFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount

  products = DjangoFilterConnectionField(lambda: StoreProductNode, filterset_class=StoreProductFilter)

  def resolve_products(self, info, **kwargs):
    return StoreProduct.objects.filter(store=self)


class StoreCategoryNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = StoreCategory
    fields = ['uid', 'name', 'color', 'created_at', 'updated_at']
    filterset_class = StoreCategoryFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class StoreSectionNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = StoreSection
    fields = ['uid', 'name', 'section_type', 'created_at', 'updated_at']
    filterset_class = StoreSectionFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class StoreSectionTypeNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = StoreSectionType
    fields = ['uid', 'name', 'created_at', 'updated_at']
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class StoreProductNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = StoreProduct
    fields = ['store', 'product', 'price', 'section', 'created_at', 'updated_at']
    filterset_class = StoreProductFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount
