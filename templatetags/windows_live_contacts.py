from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from ..utils import windows_live_get_state

register = template.Library()

@register.simple_tag
def windows_live_auth_url(request, wll, state):
    state = windows_live_get_state(request, wll)
    if not state:
        return 'http://login.live.com/wlogin.srf?appid=%s&alg=wsignin1.0' % wll.getAppId()
    elif state == 'authenticated':
        return wll.getConsentUrl(settings.WINDOWS_LIVE_OFFERS)
    else:
        return reverse('windows_live_contacts_logout')
