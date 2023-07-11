import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from api.permissions import IsAuthenticated
from shop.models import (
  Product,
  Store,
  List,
)

class ProductNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = Product
    filter_fields = ['uid', 'name', 'category', 'created_at', 'updated_at']
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False


class StoreNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = Store
    filter_fields = ['uid', 'name', 'category', 'products', 'created_at', 'updated_at']
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False


class ListNode(IsAuthenticated, DjangoObjectType):
  class Meta:
    model = List
    filter_fields = ['uid', 'name', 'category', 'products', 'created_at', 'updated_at']
    interfaces = (graphene.relay.Node, )
    convert_choices_to_enum = False
