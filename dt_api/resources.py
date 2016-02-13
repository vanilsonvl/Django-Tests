from django.contrib.auth.models import User
from push_notifications.models import GCMDevice, APNSDevice
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from .authentication import EmailAuthentication
from dt_custom_user.models import CustomUser
from tastypie.validation import Validation
from tastypie.fields import ForeignKey

class UserValidationResource(ModelResource):
    class Meta:
        queryset = CustomUser.objects.all()
	resource_name = 'auth'
	authentication = BasicAuthentication()
	authorization = Authorization()
	
    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id).select_related()


class UserResource(ModelResource):
    class Meta:
	queryset = CustomUser.objects.all().select_related('api_key')
	authentication = MultiAuthentication(EmailAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
	exclude = ['password']


    def dehydrate(self, bundle):
        user = bundle.request.user
        if bundle.obj.pk == user.pk:
            bundle.data['key'] = bundle.obj.api_key.key
            user.last_login = datetime.now(pytz.timezone(TIME_ZONE))
            user.save()

        if hasattr(user, 'driver'):
            bundle.data['is_driver'] = True
            bundle.data['is_receptive'] = False
        elif hasattr(user, 'receptive'):
            bundle.data['is_driver'] = False
            bundle.data['is_receptive'] = True
        else:
            bundle.data['is_driver'] = False
            bundle.data['is_receptive'] = False
        return bundle

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id).select_related()


class TokenValidation(Validation):
    def is_valid(self, bundle, request=None):

        errors = {}

        if GCMDevice.objects.filter(registration_id=bundle.data['registration_id']).exists() or \
                APNSDevice.objects.filter(registration_id=bundle.data['registration_id']).exists():
            errors['registration_id'] = 'Already on database'
        return errors


class GCMDeviceResource(ModelResource):
    user = ForeignKey(UserResource, 'user')

    class Meta:
        queryset = GCMDevice.objects.all()
        authorization = Authorization()
        validation = TokenValidation()
        authentication = ApiKeyAuthentication()

    def hydrate(self, bundle):
        bundle.data['user'] = bundle.request.user
        return bundle


class APNSDeviceResource(ModelResource):
    user = ForeignKey(User, 'user')

    class Meta:
        queryset = APNSDevice.objects.all()
        authorization = Authorization()
        validation = TokenValidation()
        authentication = ApiKeyAuthentication()

    def hydrate(self, bundle):
        bundle.data['user'] = bundle.request.user
        return bundle
