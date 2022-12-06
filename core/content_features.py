import requests
import re
import urllib


#################################################################################################################################
#               Number of hyperlinks present in a website 
#################################################################################################################################

def nb_hyperlinks(Href, Link, Media, Form, CSS, Favicon):
     return len(Href['internals']) + len(Href['externals']) +\
            len(Link['internals']) + len(Link['externals']) +\
            len(Media['internals']) + len(Media['externals']) +\
            len(Form['internals']) + len(Form['externals']) +\
            len(CSS['internals']) + len(CSS['externals']) +\
            len(Favicon['internals']) + len(Favicon['externals'])

#################################################################################################################################
#               Internal hyperlinks ratio 
# #################################################################################################################################

#Number of hyberlink in total
def h_total(Href, Link, Media, Form, CSS, Favicon):
    return nb_hyperlinks(Href, Link, Media, Form, CSS, Favicon)

def h_internal(Href, Link, Media, Form, CSS, Favicon):
    return len(Href['internals']) + len(Link['internals']) + len(Media['internals']) +\
           len(Form['internals']) + len(CSS['internals']) + len(Favicon['internals'])


def internal_hyperlinks(Href, Link, Media, Form, CSS, Favicon):
    total = h_total(Href, Link, Media, Form, CSS, Favicon)
    if total == 0:
        return 0
    else :
        return h_internal(Href, Link, Media, Form, CSS, Favicon)/total


#################################################################################################################################
#               External hyperlinks ratio (Kumar Jain'18)
#################################################################################################################################


def h_external(Href, Link, Media, Form, CSS, Favicon):
    return len(Href['externals']) + len(Link['externals']) + len(Media['externals']) +\
           len(Form['externals']) + len(CSS['externals']) + len(Favicon['externals'])
           
           
def external_hyperlinks(Href, Link, Media, Form, CSS, Favicon):
    total = h_total(Href, Link, Media, Form, CSS, Favicon)
    if total == 0:
        return 0
    else :
        return h_external(Href, Link, Media, Form, CSS, Favicon)/total


#################################################################################################################################
#               Number of null hyperlinks 
#################################################################################################################################

def h_null(hostname, Href, Link, Media, Form, CSS, Favicon):
    return len(Href['null']) + len(Link['null']) + len(Media['null']) +\
        len(Form['null']) + len(CSS['null']) + len(Favicon['null'])

def null_hyperlinks(hostname, Href, Link, Media, Form, CSS, Favicon):
    total = h_total(Href, Link, Media, Form, CSS, Favicon)
    if total==0:
        return 0
    return h_null(hostname, Href, Link, Media, Form, CSS, Favicon)/total

#################################################################################################################################
#               Extrenal CSS 
#################################################################################################################################


def external_css(CSS):
    return len(CSS['externals'])
    

#################################################################################################################################
#               Internal redirections 
#################################################################################################################################
from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from http import HTTPStatus
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
 
# Check if website is redirect or not
def is_redirect(url):
    try:
        r = requests.get(url, timeout=3)
        if (len(r.history > 0)):
            return 1
    except:
        return 0
 
# Get request return code of url 
def is_error(url):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code >= 400:
            return 1
    except:
        return 0
 
#Count number of redirect url
def check_urls_is_redirect(urls):
    count = 0
    with ThreadPoolExecutor(20) as executor:
        future_to_url = {executor.submit(is_redirect, url):url for url in urls}
        for future in as_completed(future_to_url):
            if isinstance(future.result(), int):
                count += future.result()
    return count


#Count number of error url
def check_urls_is_error(urls):
    count = 0
    with ThreadPoolExecutor(20) as executor:
        future_to_url = {executor.submit(is_error, url):url for url in urls}
        for future in as_completed(future_to_url):
            if isinstance(future.result(), int):
                count += future.result()
    return count

#Just handel internal link then check redirect
def h_i_redirect(Href, Link, Media, Form, CSS, Favicon):

    internal_link = []
    internal_link.extend(Href['internals'])
    internal_link.extend(Link['internals'])
    internal_link.extend(Media['internals'])
    internal_link.extend(Form['internals'])
    internal_link.extend(CSS['internals'])
    internal_link.extend(Favicon['internals'])

    return check_urls_is_redirect(internal_link)



def internal_redirection(Href, Link, Media, Form, CSS, Favicon):
    internals = h_internal(Href, Link, Media, Form, CSS, Favicon)
    if (internals > 0):
        return h_i_redirect(Href, Link, Media, Form, CSS, Favicon)/internals
    return 0

#################################################################################################################################
#               External redirections 
##################################################################################################################################
def h_e_redirect(Href, Link, Media, Form, CSS, Favicon):

    external_link = []
    external_link.extend(Href['externals'])
    external_link.extend(Link['externals'])
    external_link.extend(Media['externals'])
    external_link.extend(Form['externals'])
    external_link.extend(CSS['externals'])
    external_link.extend(Favicon['externals'])

    return check_urls_is_redirect(external_link)


def external_redirection(Href, Link, Media, Form, CSS, Favicon):
    externals = h_external(Href, Link, Media, Form, CSS, Favicon)
    if (externals > 0):
        return h_e_redirect(Href, Link, Media, Form, CSS, Favicon)/externals
    return 0



#################################################################################################################################
#               Generates internal errors 
##################################################################################################################################

def h_i_error(Href, Link, Media, Form, CSS, Favicon):

    internals_link = []
    internals_link.extend(Href['internals'])
    internals_link.extend(Link['internals'])
    internals_link.extend(Media['internals'])
    internals_link.extend(Form['internals'])
    internals_link.extend(CSS['internals'])
    internals_link.extend(Favicon['internals'])

    return check_urls_is_error(internals_link)
    

def internal_errors(Href, Link, Media, Form, CSS, Favicon):
    internals = h_internal(Href, Link, Media, Form, CSS, Favicon)
    if (internals > 0):
        return h_i_error(Href, Link, Media, Form, CSS, Favicon)/internals
    return 0

#################################################################################################################################
#               Using multiple thred to get number of external link error
# #################################################################################################################################
def h_e_error(Href, Link, Media, Form, CSS, Favicon):

    external_link = []
    external_link.extend(Href['externals'])
    external_link.extend(Link['externals'])
    external_link.extend(Media['externals'])
    external_link.extend(Form['externals'])
    external_link.extend(CSS['externals'])
    external_link.extend(Favicon['externals'])

    return check_urls_is_error(external_link)


def external_errors(Href, Link, Media, Form, CSS, Favicon):
    externals = h_external(Href, Link, Media, Form, CSS, Favicon)
    if (externals > 0):
        return h_e_error(Href, Link, Media, Form, CSS, Favicon)/externals
    return 0


#################################################################################################################################
#               Having login form link (Kumar Jain'18)
#################################################################################################################################

def login_form(Form):
    p = re.compile('([a-zA-Z0-9\_])+.php')
    if len(Form['externals'])>0 or len(Form['null'])>0:
        return 1
    for form in Form['internals']+Form['externals']:
        if p.match(form) != None :
            return 1
    return 0

#################################################################################################################################
#               Having external favicon (Kumar Jain'18)
#################################################################################################################################

def external_favicon(Favicon):
    if len(Favicon['externals'])>0:
        return 1
    return 0


#################################################################################################################################
#               Submitting to email 
#################################################################################################################################

def submitting_to_email(Form):
    for form in Form['internals'] + Form['externals']:
        if "mailto:" in form or "mail()" in form:
            return 1
        else:
            return 0
    return 0


#################################################################################################################################
#               Percentile of internal media <= 61 : Request URL in Zaini'2019 
#################################################################################################################################

def internal_media(Media):
    total = len(Media['internals']) + len(Media['externals'])
    internals = len(Media['internals'])
    try:
        percentile = internals / float(total) * 100
    except:
        return 0
    
    return percentile

#################################################################################################################################
#               Percentile of external media : Request URL in Zaini'2019 
#################################################################################################################################

def external_media(Media):
    total = len(Media['internals']) + len(Media['externals'])
    externals = len(Media['externals'])
    try:
        percentile = externals / float(total) * 100
    except:
        return 0
    
    return percentile

#################################################################################################################################
#               Check for empty title 
#################################################################################################################################

def empty_title(Title):
    if Title:
        return 0
    return 1


#################################################################################################################################
#               Percentile of safe anchor 
#################################################################################################################################

def safe_anchor(Anchor):
    total = len(Anchor['safe']) +  len(Anchor['unsafe'])
    unsafe = len(Anchor['unsafe'])
    try:
        percentile = unsafe / float(total) * 100
    except:
        return 0
    return percentile 

#################################################################################################################################
#               Percentile of internal links 
#################################################################################################################################

def links_in_tags(Link):
    total = len(Link['internals']) +  len(Link['externals'])
    internals = len(Link['internals'])
    try:
        percentile = internals / float(total) * 100
    except:
        return 0
    return percentile

#################################################################################################################################
#              IFrame Redirection
#################################################################################################################################

def iframe(IFrame):
    if len(IFrame['invisible'])> 0: 
        return 1
    return 0

#################################################################################################################################
#              Onmouse action
#################################################################################################################################

def onmouseover(content):
    if 'onmouseover="window.status=' in str(content).lower().replace(" ",""):
        return 1
    else:
        return 0

#################################################################################################################################
#              Pop up window
#################################################################################################################################

def popup_window(content):
    if "prompt(" in str(content).lower():
        return 1
    else:
        return 0

#################################################################################################################################
#              Right_clic action
#################################################################################################################################

def right_clic(content):
    if re.findall(r"event.button ?== ?2", content):
        return 1
    else:
        return 0


#################################################################################################################################
#              Domain in page title 
#################################################################################################################################

def domain_in_title(domain, title):
    if (isinstance(domain, str) and (isinstance(title, str))):
        if domain.lower() in title.lower(): 
            return 0
    return 1

#################################################################################################################################
#              Domain after copyright logo 
#################################################################################################################################

def domain_with_copyright(domain, content):
    try:
        m = re.search(u'(\N{COPYRIGHT SIGN}|\N{TRADE MARK SIGN}|\N{REGISTERED SIGN})', content)
        _copyright = content[m.span()[0]-50:m.span()[0]+50]
        if domain.lower() in _copyright.lower():
            return 0
        else:
            return 1 
    except:
        return 0
