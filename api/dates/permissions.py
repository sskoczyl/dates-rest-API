from rest_framework.permissions import BasePermission

from api.settings import X_API_KEY


class HasAPIHeader(BasePermission):
    def has_permission(self, request, view):
        return request.headers.get("X-API-KEY") == X_API_KEY
