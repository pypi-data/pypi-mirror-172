from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from dry_rest_permissions.generics import authenticated_users

from django_keycloak.keycloak import Connect
from .managers import KeycloakUserManager, KeycloakUserManagerAutoId


class AbstractKeycloakUser(AbstractBaseUser, PermissionsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_user_info = None

    id = models.UUIDField(_("keycloak_id"), unique=True, primary_key=True)
    username = models.CharField(_("username"), unique=True, max_length=20)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True)

    USERNAME_FIELD = "username"

    objects = KeycloakUserManager()

    @property
    def keycloak_identifier(self):
        return self.id

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta(AbstractBaseUser.Meta):
        abstract = True

    def update_keycloak(self, email=None, first_name=None, last_name=None):
        keycloak = Connect()
        values = {}
        if email is not None:
            values["email"] = email
        if first_name is not None:
            values["firstName"] = first_name
        if last_name is not None:
            values["lastName"] = last_name
        return keycloak.update_user(self.keycloak_identifier, **values)

    def delete_keycloak(self):
        keycloak = Connect()
        keycloak.delete_user(self.keycloak_identifier)


class KeycloakUser(AbstractKeycloakUser):
    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def email(self):
        self._confirm_cache()
        return self._cached_user_info.get("email")

    @property
    def first_name(self):
        self._confirm_cache()
        return self._cached_user_info.get("firstName")

    @property
    def last_name(self):
        self._confirm_cache()
        return self._cached_user_info.get("lastName")

    def _confirm_cache(self):
        if not self._cached_user_info:
            keycloak = Connect()
            self._cached_user_info = keycloak.get_user_info_by_id(self.id)


class AbstractKeycloakUserAutoId(AbstractKeycloakUser):
    """
    This AbstractModel uses the default django AutoIncrement field as the PK,
    opposed to the AbstractKeycloakUser wich uses keycloak_id as the table PK.
    This will allow for an easier migration of keycloak server if needed

    WARN: AbstractKeycloakUser is not updatable to this one since it will break
          all relationships, You should reset the db or edit all relationships
          manually
    """

    id = models.AutoField(primary_key=True)
    keycloak_id = models.UUIDField(_("keycloak_id"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)

    objects = KeycloakUserManagerAutoId()

    @property
    def keycloak_identifier(self):
        return self.keycloak_id

    def _confirm_cache(self):
        if not self._cached_user_info:
            keycloak = Connect()
            self._cached_user_info = keycloak.get_user_info_by_id(self.keycloak_id)

    class Meta:
        abstract = True

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @authenticated_users
    def has_object_update_permission(self, request):
        return self == request.user

    @authenticated_users
    def has_object_retrieve_permission(self, request):
        return self == request.user

    @staticmethod
    @authenticated_users
    def permission_filter(request):
        return Q(username=request.user.username)


class KeycloakUserAutoId(AbstractKeycloakUserAutoId):
    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
