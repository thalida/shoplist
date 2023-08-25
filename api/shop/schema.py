import graphene
from graphene_django.filter import DjangoFilterConnectionField
from api.graphql import RelayUUIDNode

from shop.graphql.nodes import (
    ProductNode,
    ProductCategoryNode,
    ProductUnitNode,
    StoreNode,
    StoreCategoryNode,
    StoreSectionNode,
)

from shop.graphql.mutations import (
    CreateProduct,
    CreateProductCategory,
    UpdateProduct,
    DeleteProduct,
)

class ShopQuery(graphene.ObjectType):
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
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

    create_product_category = CreateProductCategory.Field()
