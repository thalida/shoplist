import graphene
from graphene_django.types import DjangoObjectType
import graphql_jwt
from graphql_jwt.settings import jwt_settings
from social_django.utils import load_strategy, load_backend
from api.permissions import IsAuthenticated
from .models import User


class UserNode(IsAuthenticated, DjangoObjectType):
    class Meta():
        model = User
        filter_fields = ["uid", "username", "email"]
        exclude = ["email", "password"]
        interfaces = (graphene.relay.Node, )


class RegisterFromSocial(graphene.relay.ClientIDMutation):
    class Input:
        access_token = graphene.String(required=True)
        social_backend = graphene.String(required=True)

    user = graphene.Field(UserNode)
    token = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        social_strategy = load_strategy()
        social_backend = load_backend(
            social_strategy,
            input['social_backend'],
            redirect_uri=None
        )
        user = social_backend.do_auth(input['access_token'])

        payload = jwt_settings.JWT_PAYLOAD_HANDLER(user, info.context)
        token = jwt_settings.JWT_ENCODE_HANDLER(payload, info.context)

        return RegisterFromSocial(user=user, token=token)


class UserQuery(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserNode)
    me = graphene.Field(UserNode)

    def resolve_me(self, info):
        if info.context.user.is_anonymous:
            raise Exception('403: Unauthorized')

        return info.context.user


class UserMutation(graphene.ObjectType):
    token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()
    revoke_token = graphql_jwt.relay.Revoke.Field()
    register_social = RegisterFromSocial.Field()
