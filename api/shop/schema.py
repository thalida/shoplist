import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from api.graphql import RelayUUIDNode

from shop.graphql.nodes import (
    ListNode,
    ListCategoryNode,
    ProductNode,
    ProductCategoryNode,
    ProductUnitNode,
    StoreNode,
    StoreCategoryNode,
    StoreSectionNode,
)

from shop.graphql.mutations import (
    CreateProduct,
)

class ShopQuery(graphene.ObjectType):
    list = RelayUUIDNode.Field(ListNode)
    all_lists = DjangoFilterConnectionField(ListNode)

    list_category = RelayUUIDNode.Field(ListCategoryNode)
    all_list_categories = DjangoFilterConnectionField(ListCategoryNode)

    product = RelayUUIDNode.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)

    product_category = RelayUUIDNode.Field(ProductCategoryNode)
    all_product_categories = DjangoFilterConnectionField(ProductCategoryNode)

    product_unit = RelayUUIDNode.Field(ProductUnitNode)
    all_product_units = DjangoFilterConnectionField(ProductUnitNode)

    store = RelayUUIDNode.Field(StoreNode)
    all_stores = DjangoFilterConnectionField(StoreNode)

    store_category = RelayUUIDNode.Field(StoreCategoryNode)
    all_store_categories = DjangoFilterConnectionField(StoreCategoryNode)

    store_section = RelayUUIDNode.Field(StoreSectionNode)
    all_store_sections = DjangoFilterConnectionField(StoreSectionNode)



class ShopMutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
