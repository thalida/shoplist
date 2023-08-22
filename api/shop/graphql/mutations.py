import graphene

from api.permissions import login_required
from shop.models import (
    Product,
    Store,
    List,
)
from shop.graphql.nodes import (
    ProductNode,
    StoreNode,
    ListNode,
)


class CreateProduct(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        categories = graphene.List(graphene.UUID, required=False)
        stores = graphene.List(graphene.UUID, required=False)
        lists = graphene.List(graphene.UUID, required=False)

    product = graphene.Field(ProductNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        product = Product.objects.create(
            name=input.get('name', None)
        )

        for k, v in input.items():
            if k == 'name':
                continue

            if k == 'categories':
                product.categories.set(v)
                continue

            if k == 'stores':
                product.stores.set(v)
                continue

            if k == 'lists':
                product.lists.set(v)
                continue

        product.save()

        return CreateProduct(product=product)
