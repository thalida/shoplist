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

    product = graphene.Field(ProductNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        product = Product.objects.create(
            owner=info.context.user,
            title=input.get('name', None)
        )

        return CreateProduct(product=product)
