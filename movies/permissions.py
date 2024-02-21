from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request: Request, view: APIView):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        return False
