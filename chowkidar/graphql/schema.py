import graphene

from chowkidar.auth import authenticate_user_from_credentials
from .decorators import login_required
from ..utils import AuthError


class AuthenticatedUser(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()


class GenerateTokenResponse(graphene.ObjectType):
    success = graphene.Boolean()
    user = graphene.Field('user.graphql.types.user.PersonalProfile')


class AuthenticateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=False, description="Email address of the user")
        username = graphene.String(required=False, description="Username of the user")
        password = graphene.String(required=True, description="Password of the user")

    Output = GenerateTokenResponse

    def mutate(self, info, password, email=None, username=None):
        user = authenticate_user_from_credentials(password=password, email=email, username=username)
        return {"success": True, "user": user}


class LogoutUser(graphene.Mutation):

    Output = graphene.Boolean

    @login_required
    def mutate(self, info):
        return True


class SocialAuth(graphene.Mutation):
    class Arguments:
        accessToken = graphene.String(required=True, description='Access Token from Client')
        provider = graphene.String(required=True, description='Auth Provider')

    Output = GenerateTokenResponse

    def mutate(self, info, accessToken, provider):
        from social_core.exceptions import MissingBackend
        from social_django.views import _do_login
        from social_django.utils import load_backend, load_strategy
        try:
            strategy = load_strategy(info.context)
            backend = load_backend(strategy, provider, redirect_uri=None)
        except MissingBackend:
            raise AuthError('Auth Provider Not Supported', code='INVALID_PROVIDER')

        user = backend.do_auth(accessToken, user=None)
        _do_login(backend, user, user.social_user)
        return {"success": True, "user": user.__dict__}


class AuthMutations(graphene.ObjectType):
    authenticateUser = AuthenticateUser.Field()
    logoutUser = LogoutUser.Field()
    socialAuth = SocialAuth.Field()


__all__ = [
    'AuthMutations'
]
