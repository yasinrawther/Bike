from django.conf.urls import patterns, include, url
from django.contrib import admin
from bikedetails.views import *
admin.autodiscover()
v1  = Api(api_name="bike")

v1.register(AdminResource())
v1.register(DataApi())
v1.register(AdminResource())
v1.register(VendorResource())
v1.register(SupervisorResource())
v1.register(UserData())

urlpatterns = patterns('',
	# Examples:
    # url(r'^$', 'bike.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', get_image),
    url(r'^save_details/', save_details),
    url(r'^view_details/',detail_view),

    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1.urls)),

)
