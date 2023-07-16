import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from api.graphql import RelayUUIDNode

from shop.graphql.nodes import (
    ProductCategoryNode,
    ListCategoryNode,
    StoreCategoryNode,
    ProductUnitNode,
    ProductNode,
    StoreNode,
    ListNode,
)

class ShopQuery(graphene.ObjectType):
    product = RelayUUIDNode.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)

    store = RelayUUIDNode.Field(StoreNode)
    all_stores = DjangoFilterConnectionField(StoreNode)

    list = RelayUUIDNode.Field(ListNode)
    all_lists = DjangoFilterConnectionField(ListNode)

    product_category = RelayUUIDNode.Field(ProductCategoryNode)
    all_product_categories = DjangoFilterConnectionField(ProductCategoryNode)

    product_unit = RelayUUIDNode.Field(ProductUnitNode)
    all_product_units = DjangoFilterConnectionField(ProductUnitNode)

    list_category = RelayUUIDNode.Field(ListCategoryNode)
    all_list_categories = DjangoFilterConnectionField(ListCategoryNode)

    store_category = RelayUUIDNode.Field(StoreCategoryNode)
    all_store_categories = DjangoFilterConnectionField(StoreCategoryNode)



class ShopMutation(graphene.ObjectType):
    create_product = graphene.Field(ProductNode)
