# Create your views here.
import ujson

from django.conf import settings
from django.http import HttpResponse

from mds.api.responses import JSONResponse

FPATH = "/media/clients/app-android.apk"
VERSION = "2"

def version(request):
    message = VERSION
    return JSONResponse(ujson.dumps({
        'status':'SUCCESS',
        'code':200, 
        'message': message}))