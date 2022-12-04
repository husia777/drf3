from django.http import Http404
from rest_framework.permissions import BasePermission

from ads.models import Compilation, Ads, Users


class PermissionsForCompilation(BasePermission):
    message = 'Изменять и удалять подборку может только создатель'

    def has_permission(self, request, view):
        try:
            obj = Compilation.objects.get(pk=view.kwargs['pk'])
        except Compilation.DoesNotExist:
            raise Http404
        if obj.owner_id == request.user.id:
            return True
        return False


class PermissionsForAds(BasePermission):
    message = 'Изменять и удалять подборку может только создатель или Модератор, или Админ'

    def has_permission(self, request, view):
        try:
            print(view)
            print(request)
            obj = Ads.objects.get(pk=view.kwargs['pk'])
        except Compilation.DoesNotExist:
            raise Http404
        if obj.owner_id == request.user.id or request.user.role == Users.ADMIN or request.user.role == Users.M0DERATOR:
            return True
        return False
