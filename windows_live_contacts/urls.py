from django.conf.urls.defaults import *

from views import windows_live_login, windows_live_logout, windows_live_policy

urlpatterns = patterns('',

    url(r'^login/$', windows_live_login, name='windows_live_contacts_login'),
    url(r'^logout/$', windows_live_logout, name='windows_live_contacts_logout'),
    url(r'^policy/$', windows_live_policy, name='windows_live_contacts_policy'),
    
)
