windows_live_contacts
===============

Allows you to retrieve the contacts from the Windows Live (Hotmail) account
of a user of your site, via Micro$oft's APIs.

Installation instructions:

1. Place the windows_live_contacts directory somewhere in your PYTHONPATH.

2. Define the following variables in your project's settings.py file:

-----------------------------------------------------------------------------

WINDOWS_LIVE_KEYFILE = 'project/windows_live_config.xml'

(can be any location within your project directory)

WINDOWS_LIVE_OFFERS = 'Contacts.View'

(the value of this should never change)

WINDOWS_LIVE_COOKIE_LOGIN = 'windows_live_token_login'

(the value can be whatever you want, as long as it's a unique cookie name
within your project)

WINDOWS_LIVE_COOKIE_CONSENT = 'windows_live_token_consent'

(the value can be whatever you want, as long as it's a unique cookie name
within your project)

WINDOWS_LIVE_URL_BASE = 'https://livecontacts.services.live.com'

(the value of this should never change)

WINDOWS_LIVE_URL_PATH = '/users/@L@%s/rest/LiveContacts/Contacts/'

(the value of this should never change)

WINDOWS_LIVE_REDIRECT_SESSION_VAR = 'windows_live_contacts_redirect'

(the value can be whatever you want, as long as it's a unique cookie name
within your project)

3. Copy the windows_live_config.xml file into your project directory,
   in a location matching your WINDOWS_LIVE_KEYFILE setting. Change the
   appid, secret, returnurl, and policyurl values to those of your project.

-----------------------------------------------------------------------------

4. Use code similar to the following, in the view for which you want to
   display the contact import functionality:

-----------------------------------------------------------------------------

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from windows_live_contacts.utils import windows_live_get_state, windows_live_import
from windows_live_contacts.WindowsLiveLogin import WindowsLiveLogin

def test_page(request):
    request.session[settings.WINDOWS_LIVE_REDIRECT_SESSION_VAR] = request.path
    
    wll = WindowsLiveLogin.initFromXml(settings.WINDOWS_LIVE_KEYFILE)
    windows_live_contacts = windows_live_import(request, wll, cache=True)
    windows_live_state = windows_live_get_state(request, wll)
    
    return render_to_response('test_page.html', {
        'wll': wll,
        'windows_live_state': windows_live_state,
        'windows_live_contacts': windows_live_contacts
    }, context_instance=RequestContext(request))

-----------------------------------------------------------------------------

5. Use code similar to the following, in the template for which you want to
   display the contact import functionality:

-----------------------------------------------------------------------------

{% load windows_live_contacts %}

<p>
{% if windows_live_state == 'authorized' %}
  Using imported contacts from Windows Live Mail [<a
  href="{% windows_live_auth_url request wll windows_live_state %}">
  stop using</a>]
{% else %}
  Import contacts from <a
  href="{% windows_live_auth_url request wll windows_live_state %}">
  Hotmail</a>
{% endif %}
</p>

{% if windows_live_contacts %}
<ul>
  {% for contact in windows_live_contacts %}
  <li>{{ contact }}</li>
  {% endfor %}
</ul>
{% endif %}

-----------------------------------------------------------------------------
