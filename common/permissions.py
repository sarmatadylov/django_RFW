from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """
    Кастомный permission:
    - запрещает доступ, если пользователь не авторизован
    - блокирует POST для staff
    - разрешает staff любые действия с объектом
    - обычные пользователи могут работать только со своими объектами (owner)
    """

    def has_permission(self, request, view):
        #проверка авторизации
        if not request.user.is_authenticated:
            return False

        #блокируем POST для staff
        if request.method == "POST" and request.user.is_staff:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        #staff может всё
        if request.user.is_staff:
            return True

        #обычные пользователи могут работать только со своими объектами
        owner = getattr(obj, 'owner', None)
        return owner == request.user