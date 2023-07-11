import graphene

from authentication.schema import UserQuery, UserMutation
from shop.schema import ShopQuery, ShopMutation


class Query(UserQuery, ShopQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, ShopMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
