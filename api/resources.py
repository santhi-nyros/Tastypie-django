import json
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf.urls import url, include
from django.contrib.auth import authenticate, login, logout
from tastypie.authentication import (
    Authentication, ApiKeyAuthentication, BasicAuthentication,
    MultiAuthentication)
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.utils import trailing_slash
from .models import UserProfile,Entry,Recipe,Post,Comment
from .utils import MINIMUM_PASSWORD_LENGTH, validate_password
from .exceptions import CustomBadRequest
from .Rserializer import urlencodeSerializer,MultiPartResource




class UserResource(ModelResource):
    raw_password = fields.CharField(attribute=None, readonly=True, null=True, blank=True)

    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get', 'post' ]
        resource_name = 'user'
        authentication = Authentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json'])


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view("login"), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view("logout"), name="api_logout"),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        username = data.get('username', '')
        password = data.get('password', '')


        user = authenticate(username=username, password=password)
        # print user
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpUnauthorized)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)


    def logout(self, request, **kwargs):
        """
        Attempt to log a user out, and return success status.
        """
        self.method_check(request, allowed=['get'])

        # Run tastypie's BasicAuthentication
        self.is_authenticated(request)

        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False, 'error_message': 'You are not authenticated, %s' % request.user.is_authenticated() })




#--------------------------------------------------------------------------

class CreateUserResource(ModelResource):
    user = fields.ForeignKey('core.api.UserResource', 'user', full=True)

    class Meta:
        allowed_methods = ['post']
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        queryset = UserProfile.objects.all()
        resource_name = 'create_user'
        always_return_data = True
        serializer = Serializer(formats=['json'])

    def hydrate(self, bundle):
        REQUIRED_USER_PROFILE_FIELDS = ("birth_year", "gender", "user")
        for field in REQUIRED_USER_PROFILE_FIELDS:
            if field not in bundle.data:
                raise CustomBadRequest(
                    code="missing_key",
                    message="Must provide {missing_key} when creating a user."
                            .format(missing_key=field))

        REQUIRED_USER_FIELDS = ("username", "email", "first_name", "last_name",
                                "raw_password")
        for field in REQUIRED_USER_FIELDS:
            if field not in bundle.data["user"]:
                raise CustomBadRequest(
                    code="missing_key",
                    message="Must provide {missing_key} when creating a user."
                            .format(missing_key=field))
        return bundle

    def obj_create(self, bundle, **kwargs):
        try:
            email = bundle.data["user"]["email"]
            username = bundle.data["user"]["username"]
            if User.objects.filter(email=email):
                raise CustomBadRequest(
                    code="duplicate_exception",
                    message="That email is already used.")
            if User.objects.filter(username=username):
                raise CustomBadRequest(
                    code="duplicate_exception",
                    message="That username is already used.")
        except KeyError as missing_key:
            raise CustomBadRequest(
                code="missing_key",
                message="Must provide {missing_key} when creating a user."
                        .format(missing_key=missing_key))
        except User.DoesNotExist:
            pass

        # setting resource_name to `user_profile` here because we want
        # resource_uri in response to be same as UserProfileResource resource
        self._meta.resource_name = UserProfileResource._meta.resource_name
        return super(CreateUserResource, self).obj_create(bundle, **kwargs)


# class UserResource(ModelResource):
#     # We need to store raw password in a virtual field because hydrate method
#     # is called multiple times depending on if it's a POST/PUT/PATCH request
#     raw_password = fields.CharField(attribute=None, readonly=True, null=True,
#                                     blank=True)

#     class Meta:
#         # For authentication, allow both basic and api key so that the key
#         # can be grabbed, if needed.
#         authentication = MultiAuthentication(
#             BasicAuthentication(),
#             ApiKeyAuthentication())
#         authorization = Authorization()

#         # Because this can be updated nested under the UserProfile, it needed
#         # 'put'. No idea why, since patch is supposed to be able to handle
#         # partial updates.
#         allowed_methods = ['get', 'patch', 'put', ]
#         always_return_data = True
#         queryset = User.objects.all().select_related("api_key")
#         excludes = ['is_active', 'is_staff', 'is_superuser', 'date_joined',
#                     'last_login']
#         serializer = Serializer(formats=['json'])

#     def authorized_read_list(self, object_list, bundle):
#         return object_list.filter(id=bundle.request.user.id).select_related()

#     def hydrate(self, bundle):
#         if "raw_password" in bundle.data:
#             # Pop out raw_password and validate it
#             # This will prevent re-validation because hydrate is called
#             # multiple times
#             # https://github.com/toastdriven/django-tastypie/issues/603
#             # "Cannot resolve keyword 'raw_password' into field." won't occur

#             raw_password = bundle.data.pop["raw_password"]

#             # Validate password
#             if not validate_password(raw_password):
#                 if len(raw_password) < MINIMUM_PASSWORD_LENGTH:
#                     raise CustomBadRequest(
#                         code="invalid_password",
#                         message=(
#                             "Your password should contain at least {length} "
#                             "characters.".format(length=
#                                                  MINIMUM_PASSWORD_LENGTH)))
#                 raise CustomBadRequest(
#                     code="invalid_password",
#                     message=("Your password should contain at least one number"
#                              ", one uppercase letter, one special character,"
#                              " and no spaces."))

#             bundle.data["password"] = make_password(raw_password)

#         return bundle

#     def dehydrate(self, bundle):
#         bundle.data['key'] = bundle.obj.api_key.key

#         try:
#             # Don't return `raw_password` in response.
#             del bundle.data["raw_password"]
#         except KeyError:
#             pass

#         return bundle


class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(
            BasicAuthentication(),
            ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get', 'patch', ]
        detail_allowed_methods = ['get', 'patch', 'put']
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'
        serializer = Serializer(formats=['json'])

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user).select_related()

    ## Since there is only one user profile object, call get_detail instead
    def get_list(self, request, **kwargs):
        kwargs["pk"] = request.user.profile.pk
        return super(UserProfileResource, self).get_detail(request, **kwargs)


class EntryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        serializer = Serializer(formats=['json'])


class RecipeResource(ModelResource):
    class Meta:
        queryset = Recipe.objects.all()
        resource_name = 'recipes'
        allowed_methods = ['get']
        include_resource_uri = False
        serializer = Serializer(formats=['json'])

        def alter_list_data_to_serialize(self, request, data_dict):
            if isinstance(data_dict, dict):
                if 'meta' in data_dict:
                    #Get rid of the meta object
                    del(data_dict['meta'])

            return data_dict



class PostResource(MultiPartResource,ModelResource):
    image = fields.FileField(attribute="image", null=True, blank=True)
    video = fields.FileField(attribute="video", null=True, blank=True)
    # comments = fields.ToManyField(CommentResource, 'comments', full=True)


    class Meta:
        queryset = Post.objects.all().order_by('-created')
        resource_name = 'posts'
        serializer = Serializer(formats=['json'])
        allowed_methods = ['get','post']
        always_return_data=True
        authorization = Authorization()


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>.*?)/get_comments%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_comments'), name="api_get_comments"),
        ]

    def get_comments(self, request, **kwargs):
        post = Post.objects.filter(id = kwargs['pk']).first()
        queryset = post.get_comments()
        return self.create_response(request, {
                    'success': True,
                    'objects':list(queryset)
        })



class CommentResource(ModelResource):
    post_id = fields.ForeignKey(PostResource, 'post_id')

    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comments'
        serializer = Serializer(formats=['json'])
        allowed_methods = ['get','post']
        always_return_data=True
        authorization = Authorization()
