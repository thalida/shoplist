import copy
import graphene

from api.permissions import login_required
from shop.models import (
    Product,
    ProductCategory,
    Store,
    StoreSection,
)
from shop.graphql.nodes import (
    ProductCategoryNode,
    ProductNode,
)

class CreateProductCategory(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        color = graphene.String(required=False)

    product_category = graphene.Field(ProductCategoryNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        product_category = ProductCategory.objects.create(
            name=input.get('name'),
        )

        for k, v in input.items():
            if k == 'name':
                continue

            setattr(product_category, k, v)

        product_category.save()

        return CreateProductCategory(product_category=product_category)


class CreateProduct(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        categories = graphene.List(graphene.UUID, required=False)
        stores = graphene.List(graphene.JSONString, required=False)

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
                product.stores.clear()
                for storeProduct in v:
                    store = Store.objects.get(uid=storeProduct.get('store', None))

                    try:
                        store_section = StoreSection.objects.get(uid=storeProduct.get('section', None))
                    except StoreSection.DoesNotExist:
                        store_section = None

                    product.stores.add(
                        store,
                        through_defaults={
                            'price': storeProduct.get('price', None),
                            'section': store_section,
                        }
                    )
                continue

            setattr(product, k, v)

        product.save()

        return CreateProduct(product=product)


class UpdateProduct(graphene.relay.ClientIDMutation):
    class Input:
        uid = graphene.UUID(required=True)
        name = graphene.String(required=False)
        categories = graphene.List(graphene.UUID, required=False)
        stores = graphene.List(graphene.JSONString, required=False)

    product = graphene.Field(ProductNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        product = Product.objects.get(uid=input.get('uid', None))

        for k, v in input.items():
            if k == 'uid':
                continue

            if k == 'categories':
                product.categories.set(v)
                continue

            if k == 'stores':
                product.stores.clear()
                for storeProduct in v:
                    store = Store.objects.get(uid=storeProduct.get('store', None))

                    try:
                        store_section = StoreSection.objects.get(uid=storeProduct.get('section', None))
                    except StoreSection.DoesNotExist:
                        store_section = None

                    product.stores.add(
                        store,
                        through_defaults={
                            'price': storeProduct.get('price', None),
                            'section': store_section,
                        }
                    )
                continue

            setattr(product, k, v)

        product.save()

        return UpdateProduct(product=product)


class DeleteProduct(graphene.relay.ClientIDMutation):
    class Input:
        uid = graphene.UUID(required=True)

    product = graphene.Field(ProductNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        product = Product.objects.get(uid=input.get('uid', None))

        productCopy = copy.deepcopy(product)
        product.delete()

        return DeleteProduct(product=productCopy)
