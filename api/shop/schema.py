import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from shop.graphql.nodes import (
    ProductCategoryNode,
    ProductNode,
    StoreNode,
    ListNode,
)

class ShopQuery(graphene.ObjectType):
    product = graphene.relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)

    store = graphene.relay.Node.Field(StoreNode)
    all_stores = DjangoFilterConnectionField(StoreNode)

    list = graphene.relay.Node.Field(ListNode)
    all_lists = DjangoFilterConnectionField(ListNode)

    product_category = graphene.relay.Node.Field(ProductCategoryNode)
    all_product_categories = DjangoFilterConnectionField(ProductCategoryNode)


class ShopMutation(graphene.ObjectType):
    create_product = graphene.Field(ProductNode)
