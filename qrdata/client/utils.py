from django.http import response
from django.http.response import ResponseHeaders
#import qrcode
from io import BytesIO, StringIO



from django.http import HttpResponse
from django.template.loader import get_template
from client.models import *
from django.contrib.staticfiles import finders
import os

from xhtml2pdf import pisa
from xhtml2pdf.document import pisaDocument
from django.core.files.base import ContentFile, File
from django.conf import settings
from django.http import response
from django.http.response import ResponseHeaders
#import qrcode
from io import BytesIO, StringIO



from django.http import HttpResponse
from django.template.loader import get_template
from client.models import *
from django.contrib.staticfiles import finders
import os

from xhtml2pdf import pisa
from xhtml2pdf.document import pisaDocument
from django.core.files.base import ContentFile, File
from django.conf import settings
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL     # Typically /static/
    #static Root
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)
    return path

    '''elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))'''
    
    # make sure that file exists
    #if not os.path.isfile(path):
            #raise Exception(
                #'media URI must start with %s or %s' % (sUrl, mUrl)
            #)
    
def render_to_pdf(id,template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=link_callback)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None