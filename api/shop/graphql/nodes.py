import graphene
from graphene_django import DjangoObjectType

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
)

class ProductCategoryNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = ProductCategory
    fields = ['uid', 'name', 'created_at', 'updated_at']
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class StoreCategoryNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = StoreCategory
    fields = ['uid', 'name', 'created_at', 'updated_at']
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class ListCategoryNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = ListCategory
    fields = ['uid', 'name', 'created_at', 'updated_at']
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

class ProductNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = Product
    fields = ['uid', 'name', 'category', 'stores', 'lists', 'created_at', 'updated_at']
    filterset_class = ProductFilter
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
    connection_class = ConnectionWithTotalCount


class StoreNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = Store
    fields = ['uid', 'name', 'category', 'products', 'created_at', 'updated_at']
    filter_fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains', 'istartswith'],
      'category': ['exact'],
    }
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


class ListNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = List
    fields = ['uid', 'name', 'category', 'products', 'created_at', 'updated_at']
    filter_fields = {
      'uid': ['exact'],
      'name': ['exact', 'icontains', 'istartswith'],
      'category': ['exact'],
    }
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
