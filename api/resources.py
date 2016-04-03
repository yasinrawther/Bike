from tastypie.resources import ModelResource, Resource
from bikedetails.models import *
from django.contrib.auth.models import User
from tastypie.authentication import Authentication
from django.core.exceptions import ObjectDoesNotExist
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpCreated, HttpBadRequest, HttpResponse
from random import randint


class dict2obj(object):
  def __init__(self, initial=None):
    self.__dict__['_data'] = {}

    if hasattr(initial, 'items'):
      self.__dict__['_data'] = initial

  def __getattr__(self, name):
    return self._data.get(name, None)

  def __setattr__(self, name, value):
    self.__dict__['_data'][name] = value

  def to_dict(self):
    return self._data

class DataApi(Resource):
    username = fields.CharField(attribute='username', default=None)
    user_role = fields.CharField(attribute='user_role', default=None)
    mobile = fields.IntegerField(attribute='mobile', default=None)
    location = fields.CharField(attribute='location', default=None)
    city = fields.CharField(attribute='city', default=None)
    state = fields.CharField(attribute='state', default=None)
    booking_no = fields.CharField(attribute='booking_no', default=None)
    time_period = fields.IntegerField(attribute='time_period', default=None)
    bike_reg_no = fields.CharField(attribute='bike_reg_no', default=None)
    bike_model = fields.CharField(attribute='bike_model', default=None)
    image = fields.ImageField(attribute='image', default=None)
    km_driven = fields.IntegerField(attribute='km_driven', default=None)
    class Meta:
        resource_name = 'data'
        object_class = dict2obj

class AdminResource(DataApi):
    class Meta:
        resource_name = 'admin'
        object_class = dict2obj
        include_resource_uri = False
        authentication = Authentication()

    def obj_get_list(self, bundle, **kwargs):
        admin = Admin.objects.get(user_profile__user=bundle.request.user)
        users_data = [{'username': i.user, 'user_role': i.role, 'mobile': i.mobile, 'location': i.location, 'city': i.city, 'state': i.state} for i in UserProfile.objects.filter(admin=admin)] 
        bundle = [dict2obj(data) for data in user_data]
        return bundle

    def prepend_urls(self):
        return [
              url(r'^(?P<resource_name>%s)/create_vendor%s$' %
                  (self._meta.resource_name, trailing_slash()),
                  self.wrap_view('create_vendor'), name='api_check')
             ]

    def create_vendor(self, request, **kwargs):
        data = json.loads(request.body)
        user_obj = create_userobj(data['username'], data['email'])
        user_profile = create_userprofileobj(user_obj, 'Vendor', data['mobile'], data['location'], data['city'], data['state'])
        vendor = Vendor.objects.create(user_profile=user_profile)
        return

    def create_userobj(self, username, email):
        password = '123456'
        user_obj = User.objects.create(username=username, email=email, is_active=True)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def create_userprofileobj(self, user_obj, role, mobile, location, city, state, admin=None, vendor=None, supervisor=None):
        user_profile = UserProfile.objects.create(user=user_obj, 
                                                  role=role,
                                                  mobile=mobile, 
                                                  location=location, 
                                                  city=city, 
                                                  state=state, 
                                                  admin=admin, 
                                                  vendor=vendor, 
                                                  supervisor=supervisor)
        return user_profile

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict) and 'meta' in data_dict:
            del data_dict['meta']
        return data_dict


class VendorResource(DataApi):
    class Meta:
        resource_name = 'vendor_res'
        include_resource_uri = False
        object_class = dict2obj
        authentication = Authentication()

    def obj_get_list(self, bundle, **kwargs):
        vendor = Vendor.objects.get(user_profile__user=bundle.request.user)
        users_data = [{'username': i.user, 'user_role': i.role, 'mobile': i.mobile, 'location': i.location, 'city': i.city, 'state': i.state} for i in UserProfile.objects.filter(vendor=vendor)] 
        bundle = [dict2obj(data) for data in user_data]
        return bundle

    def prepend_urls(self):
        return [
              url(r'^(?P<resource_name>%s)/create_supervisor%s$' %
                  (self._meta.resource_name, trailing_slash()),
                  self.wrap_view('create_supervisor'), name='api_check')
             ]

    def create_supervisor(self, request, **kwargs):
        data = json.loads(request.body)
        admin_res = AdminResource()
        user_obj = admin_res.create_userobj(data['username'], data['email'])
        user_profile = admin_res.create_userprofileobj(user_obj, 'SuperVisor', data['mobile'], data['location'], data['city'], data['state'])
        SuperVisor.objects.create(user_profile=user_profile)
        return

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict) and 'meta' in data_dict:
            del data_dict['meta']
        return data_dict

class SupervisorResource(DataApi):
    booking_detail = models.DictField(attribute='booking_detail', default=None)
    class Meta:
        resource_name = 'supervisor_res'
        include_resource_uri = False
        object_class = dict2obj
        authentication = Authentication()

    def obj_get_list(self, bundle, **kwargs):
        supervisor = SuperVisor.objects.get(user_profile__user=bundle.request.user)
        users_data = []
        for i in UserProfile.objects.filter(supervisor=supervisor):
            try:
                bike_detail = BikeDetails.objects.get(user_profile=i)
                bikedetail = {'bike_reg_no': bikedetail.bike_reg_no, 'bike_model': bike_detail.bike_model, 'image': bike_detail.image, 'fuel_tank_capacity': bike_detail.fuel_tank_capacity}
            except ObjectDoesNotExist:
                continue
            user_data.append({'username': i.user, 'user_role': i.role, 'mobile': i.mobile, 'location': i.location, 'city': i.city, 'state': i.state, 'booking_detail': bikedetail})
        bundle = [dict2obj(data) for data in user_data]
        return bundle

    def prepend_urls(self):
        return [
              url(r'^(?P<resource_name>%s)/edit_booking%s$' %
                  (self._meta.resource_name, trailing_slash()),
                  self.wrap_view('edit_booking'), name='api_check')
            ]

    def edit_booking(self, request, **kwargs):
        data = json.loads(request.body)
        bike = BookingDetails.objects.get(booking_no=data['booking_no'])
        bike.time_period += data['extend_time']
        bike.save()
        return
    
    def obj_delete(self, bundle, **kwargs):
        bike = BikeDetails.objects.get(booking_no=bundle.data['booking_no'])
        bike.delete()
        return

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict) and 'meta' in data_dict:
            del data_dict['meta']
        return data_dict

class UserData(DataApi):
    class Meta:
        resource_name = 'user_data'
        include_resource_uri = False
        object_class = dict2obj
        authentication = Authentication()

    def obj_get_list(self, bundle, **kwargs):
        user_profile = BookingDetails.objects.filter(user_profile__user=bundle.request.user)
        datas = [{"booking_no": i.booking_no, "time_period": i.time_period, "bike_reg_no": i.bike_detail.bike_reg_no, "bike_model": i.bike_detail.bike_model, "image": i.bike_detail.image, "km_driven": i.bike_detail.km_driven} for i in booking_detail]
        bundle = [dict2obj(data) for data in datas]
        return bundle

    def obj_create(self, bundle, **kwargs):
        data = bundle.data
        bikedetail = BikeDetails.objects.get(id=data['id'])
        booking_no = bundle.request.user.username+'_'+randint(10000, 99999)
        BookingDetails.objects.create(user_profile=bundle.request.user, bikedetail=bikedetail, time_period=data['time_period'], booking_no=booking_no)
        raise ImmediateHttpResponse(response=HttpCreated(content=json.dumps({'status': 'booking confirmed'}), content_type="application/json; charset=UTF-8"))
    
    def obj_delete(self, bundle, **kwargs):
        bike = BikeDetails.objects.get(booking_no=bundle.data['booking_no'])
        bike.delete()
        return

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict) and 'meta' in data_dict:
            del data_dict['meta']
        return data_dict




        