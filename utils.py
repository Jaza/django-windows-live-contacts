from xml.dom import minidom
import urllib2

from django.conf import settings

from windows_live_contacts.WindowsLiveLogin import WindowsLiveLogin

def windows_live_import(request, wll, cache=False):
    """
    Uses the given windows live service object to retrieve WL Contacts and
    import the entries with an email address into the contacts of the
    given user.
    
    Returns a list of 'contact name <contact@email>' strings.
    """
    state = windows_live_get_state(request, wll)
    xmldoc = None
    contacts = []
    
    if state == 'authorized':
        if cache and request.session.get('windows_live_contacts_cached'):
            return request.session.get('windows_live_contacts_cached')
        
        windows_live_consent = wll.processConsentToken(request.session.get(settings.WINDOWS_LIVE_COOKIE_CONSENT))
        
        windows_live_url_path = settings.WINDOWS_LIVE_URL_PATH % windows_live_consent.getLocationID()
        windows_live_url = '%s%s' % (settings.WINDOWS_LIVE_URL_BASE, windows_live_url_path)
        auth_header_value = 'DelegatedToken dt="%s"' % windows_live_consent.getDelegationToken()
        req = urllib2.Request(windows_live_url, None, {'Authorization': auth_header_value})
        f = urllib2.urlopen(req)
        xmldoc = minidom.parse(f)
    
    if xmldoc:
        for entry in xmldoc.getElementsByTagName('Contact'):
            name = None
            address = None
            profiles = entry.getElementsByTagName('Profiles')
            if profiles:
                profiles = profiles[0]
                personal = profiles.getElementsByTagName('Personal')
                if personal:
                    personal = personal[0]
                    first_name = personal.getElementsByTagName('FirstName')
                    if first_name:
                        first_name = first_name[0].childNodes[0].data
                    last_name = personal.getElementsByTagName('LastName')
                    if last_name:
                        last_name = last_name[0].childNodes[0].data
                    if not (first_name or last_name):
                        unique_name = personal.getElementsByTagName('UniqueName')
                        if unique_name:
                            unique_name = unique_name[0].childNodes[0].data
                            name = unique_name
                    else:
                        name = '%s %s' % (first_name, last_name)
            emails = entry.getElementsByTagName('Emails')
            if emails:
                emails = emails[0]
                email = emails.getElementsByTagName('Email')
                if email:
                    email = email[0]
                    address = email.getElementsByTagName('Address')
                    if address:
                        address = address[0].childNodes[0].data
            
            if name and address:
                contact = '%s <%s>' % (name, address)
                contacts.append(contact)
        
        if cache:
            request.session['windows_live_contacts_cached'] = contacts
    
    return contacts


def windows_live_get_state(request, wll):
    """
    Get the current login state for the Windows Live Contacts API.
    Possible states are:
    None - logged out
    authenticated - logged in
    authorized - logged in and consent granted
    """
    state = None
    
    windows_live_user = wll.processToken(request.session.get(settings.WINDOWS_LIVE_COOKIE_LOGIN))
    windows_live_userid = None
    windows_live_consent = None
    
    if windows_live_user:
        windows_live_userid = windows_live_user.getId()
    if windows_live_userid:
        state = 'authenticated'
        windows_live_consent = wll.processConsentToken(request.session.get(settings.WINDOWS_LIVE_COOKIE_CONSENT))
    
    if windows_live_consent and windows_live_consent.isValid():
        state = 'authorized'
    
    return state
