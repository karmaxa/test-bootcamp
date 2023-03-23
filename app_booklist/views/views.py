from django import http
from django import views


class Homepage(views.View):
    def get(self, request: http.HttpRequest) -> http.JsonResponse:
        return http.JsonResponse({"header text": "", "data": {}})
