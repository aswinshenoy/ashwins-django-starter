import json

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from graphene_django.views import GraphQLView as BaseGraphQLView

from django.http.response import HttpResponseNotAllowed

from ..auth import respond_handling_authentication


class HttpError(Exception):
    def __init__(self, response, message=None, *args, **kwargs):
        self.response = response
        self.message = message = message or response.content.decode()
        super(HttpError, self).__init__(message, *args, **kwargs)


class GraphQLView(BaseGraphQLView):
    schema = None
    graphiql = False
    executor = None
    backend = None
    middleware = None
    root_value = None
    pretty = False
    batch = False
    subscription_path = None

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        try:
            if request.method.lower() not in ("get", "post"):
                raise HttpError(
                    HttpResponseNotAllowed(
                        ["GET", "POST"], "GraphQL only supports GET and POST requests."
                    )
                )

            data = self.parse_body(request)
            show_graphiql = self.graphiql and self.can_display_graphiql(request, data)

            if show_graphiql:
                return render(request, "graphiql/graphiql.html")

            if self.batch:
                responses = [self.get_response(request, entry) for entry in data]
                result = "[{}]".format(",".join([response[0] for response in responses]))
                status_code = (responses and max(responses, key=lambda response: response[1])[1] or 200)
            else:
                result, status_code = self.get_response(request, data, show_graphiql)

            return respond_handling_authentication(status_code=status_code, result=json.loads(result), request=request)

        except HttpError as e:
            response = e.response
            response["Content-Type"] = "application/json"
            response.content = self.json_encode(request, {"errors": [self.format_error(e)]})
            return response


__all__ = [
    'GraphQLView'
]

