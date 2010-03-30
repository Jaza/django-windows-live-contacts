import cgi, os

from WindowsLiveLogin import WindowsLiveLogin

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
    

@csrf_exempt
@require_http_methods(['POST'])
def windows_live_login(request):
    action = request.POST.get('action')
    
    if not action:
        raise ValueError("'action' POST value is required.")
    
    wll = WindowsLiveLogin.initFromXml(settings.WINDOWS_LIVE_KEYFILE)
    
    if action == 'login':
        token = request.POST.get('stoken')
        if not token:
            raise ValueError("'token' POST value is required when 'action' is 'login'.")
        
        os.environ['QUERY_STRING'] = 'action=%s&stoken=%s' % (action, token)
        fs = cgi.FieldStorage()
        user = wll.processLogin(fs)
        if user:
            request.session[settings.WINDOWS_LIVE_COOKIE_LOGIN] = user.getToken()
            return redirect(wll.getConsentUrl(settings.WINDOWS_LIVE_OFFERS))
        
    elif action == 'delauth':
        user = None
        token = request.session[settings.WINDOWS_LIVE_COOKIE_LOGIN]
        if not token:
            raise ValueError("'token' session value is required when 'action' is 'delauth'.")
        
        user = wll.processToken(token)
        if user:
            response_code = request.POST.get('ResponseCode')
            consent_token = request.POST.get('ConsentToken')
            os.environ['QUERY_STRING'] = 'action=%s&ResponseCode=%s&ConsentToken=%s' % (action, response_code, consent_token)
            fs = cgi.FieldStorage()
            consent = wll.processConsent(fs)
            if consent and consent.isValid():
                request.session[settings.WINDOWS_LIVE_COOKIE_CONSENT] = consent.getToken()
                return redirect(request.session.get('windows_live_contacts_redirect'))
    
    raise ValueError("'action' POST value must be either 'login' or 'delauth'.")


def windows_live_logout(request):
    if request.session.get(settings.WINDOWS_LIVE_COOKIE_LOGIN):
        del request.session[settings.WINDOWS_LIVE_COOKIE_LOGIN]
    if request.session.get(settings.WINDOWS_LIVE_COOKIE_CONSENT):
        del request.session[settings.WINDOWS_LIVE_COOKIE_CONSENT]
    if request.session.get('windows_live_contacts_cached'):
        del request.session['windows_live_contacts_cached']
    return redirect(request.session.get('windows_live_contacts_redirect'))


def windows_live_policy(request):
    return render_to_response('windows_live_contacts/policy.html', context_instance=RequestContext(request))
    
