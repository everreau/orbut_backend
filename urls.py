from django.conf.urls.defaults import patterns

urlpatterns = patterns('orbut_backend.views',
                       (r'^add_job/$', 'add_job'),
                       (r'^success/(?P<pk>\d+)/$', 'success'),
                       (r'^post_json/$', 'post_json'),
                       )
