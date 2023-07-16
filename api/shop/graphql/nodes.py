import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

from api.graphql import ConnectionWithTotalCount
from api.permissions import IsAuthenticated
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
from shop.graphql.filters import (
  ProductFilter,
  ProductCategoryFilter,
  ListCategoryFilter,
  ListFilter,
  ListProductFilter,
  StoreFilter,
  StoreCategoryFilter,
  StoreProductFilter,
)

class ProductNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = Product
    fields = ['uid', 'name', 'categories', 'stores', 'lists', 'created_at', 'updated_at']
    filterset_class = ProductFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount

  lists = DjangoFilterConnectionField(lambda: ListProductNode, filterset_class=ListProductFilter)
  stores = DjangoFilterConnectionField(lambda: StoreProductNode, filterset_class=StoreProductFilter)

  def resolve_lists(self, info, **kwargs):
    return ListProduct.objects.filter(product=self)

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
    fields = ['uid', 'name', 'created_at', 'updated_at']
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class ListProductNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = ListProduct
    fields = ['list', 'product', 'quantity_have', 'quantity_needed', 'unit', 'created_at', 'updated_at']
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class StoreProductNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = StoreProduct
    fields = ['store', 'product', 'price', 'section', 'aisle', 'created_at', 'updated_at']
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class StoreNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = Store
    fields = ['uid', 'name', 'categories', 'products', 'created_at', 'updated_at']
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
    fields = ['uid', 'name', 'created_at', 'updated_at']
    filterset_class = StoreCategoryFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class ListNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = List
    fields = ['uid', 'name', 'categories', 'products', 'created_at', 'updated_at']
    filterset_class = ListFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount

  products = DjangoFilterConnectionField(lambda: ListProductNode, filterset_class=ListProductFilter)

  def resolve_products(self, info, **kwargs):
    return ListProduct.objects.filter(list=self)


class ListCategoryNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = ListCategory
    fields = ['uid', 'name', 'created_at', 'updated_at']
    filterset_class = ListCategoryFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount
