import graphene
from shop.schema import ShopQuery, ShopMutation


class Query(ShopQuery, graphene.ObjectType):
    pass


class Mutation(ShopMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
