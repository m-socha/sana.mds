'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''
import logging
import ujson

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models import Max, Q

from piston3.handler import BaseHandler
from piston3.resource import Resource

from mds.api import do_authenticate, LOGGER
from mds.api.contrib import backends

from mds.api.handlers import DispatchingHandler
from mds.api.decorators import logged, validate
from mds.api.docs.utils import handler_uri_templates
from mds.api.responses import succeed, fail, error
from mds.api.signals import EventSignal, EventSignalHandler
from mds.api.utils import logtb

from .forms import *
from .models import *

__all__ = ['ConceptHandler', 
           'RelationshipHandler',
           'RelationshipCategoryHandler',
           'DeviceHandler', 
           'EncounterHandler',
           'EventHandler',
           'LocationHandler',
           'NotificationHandler', 
           'ObservationHandler', 
           'ObserverHandler',
           'ProcedureHandler',
           'ProcedureGroupHandler',
           'DocHandler' ,
           'SessionHandler',
           'SubjectHandler',
           'LocationHandler',]

@logged     
class SessionHandler(DispatchingHandler):
    """ Handles session auth requests. """
    allowed_methods = ('GET','POST',)
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    form = SessionForm
    #model = None
    
    def create(self,request):
        try:
            content_type = request.META.get('CONTENT_TYPE', None)
            logging.debug(content_type)
            is_json = 'json' in content_type
            logging.debug("is_json: %s" % is_json)
            if is_json:
                raw_data = request.read()
                data = ujson.loads(raw_data)
            else:
                data = self.flatten_dict(request.POST)
            
            username = data.get('username', 'empty')
            password = data.get('password','empty')
            if not settings.TARGET == 'SELF':
                instance = User(username=username)
                auth = {'username':username, 'password':password }
                result = backends.create('Session', auth, instance)
                if not result:
                    return fail([],errors=["Observer does not exist",],code=404)
                # Create a user or fetch existin and update password
                user,created = User.objects.get_or_create(username=result.user.username)
                user.set_password(password)
                user.save()
                
                # should have returned an Observer instance here
                observers = Observer.objects.filter(user__username=user.username)
                # If none were returned we need to create the Observer
                if observers.count() == 0:
                    observer = Observer(
                        user=user,
                        uuid = result.uuid)
                    observer.save()
                else:
                    # Observer already exists so we don't have to do 
                    # anything since password cache is updated
                    observer = observers[0]
                return succeed(observer.uuid)
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    observer = Observer.objects.get(user=user)
                    return succeed(observer.uuid)
                else:
                    msg = "Invalid credentials"
                    logging.warn(msg)
                    return fail(msg)
        except Exception as e:
            msg = "Internal Server Error"
            logging.error(str(e))
            logtb()
            return error(msg)
        
    def read(self,request):
        success,msg = do_authenticate(request)
        if success:
            return succeed(msg)
        else:
            return fail(msg)
    
@logged
class ConceptHandler(DispatchingHandler):
    """ Handles concept requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Concept
    form = ConceptForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

class RelationshipHandler(DispatchingHandler):
    """ Handles concept relationship requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Relationship
    form = RelationshipForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
class RelationshipCategoryHandler(DispatchingHandler):
    """ Handles concept relationship category requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = RelationshipCategory
    form = RelationshipCategoryForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class DeviceHandler(DispatchingHandler):
    """ Handles device requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Device
    form = DeviceForm
    fields = (
        "uuid",
        "name",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
@logged    
class EncounterHandler(DispatchingHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Encounter
    form = EncounterForm
    fields = ("uuid",
        "concept", 
        "observation",
        ("subject",("uuid",)),
        ("procedure",("title","uuid")),
        "created",
        "modified",
        "voided",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class EventHandler(BaseHandler):
    """ Handles network request log requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Event

@logged
class NotificationHandler(DispatchingHandler):
    """ Handles notification requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Notification
    form = NotificationForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class ObservationHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST','PUT')
    model = Observation
    form = ObservationForm
    fields = (
        "uuid",
        ("encounter",("uuid")),
        "node",
        ("concept",("uuid",)),
        "value_text",
        "value_complex",
        "value",
        "created",
        "modified",
        "voided",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
@logged        
class ObserverHandler(DispatchingHandler):
    """ Handles observer requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Observer
    form = ObserverForm
    fields = (
        "uuid",
        ("user",("username","is_superuser")),
        "modified",
        "created",
        "voided",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class ProcedureHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST','PUT')
    model = Procedure
    fields = (
        "uuid",
        "title",
        "description",
        "src",
        "version",
        "author",
        "modified",
        "created",
        "voided",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
    def create(self,request, uuid=None, *args, **kwargs):
        if 'json' in request.META.get('CONTENT_TYPE', ''):
            payload = ujson.loads(request.read())
            # for now only support version, author, title, description
            valid_object = False
            supported_attributes = (
                'title',
                'author',
                'description',
                'source_file_content',
                'version'
            )
            instance = Procedure()
            for attr in supported_attributes:
                value = payload.get(attr, None)
                if value and attr != 'source_file_content':
                    setattr(instance, attr, value)
                    if attr == 'title':
                        valid_object = True
                elif value and attr == 'source_file_content':
                    instance.src.save(instance.title, ContentFile(value))
            
            if valid_object:
                instance.save()
                return succeed({'uuid':instance.uuid})
            else:
                return fail('Missing mandatory title attribute for procedure', 400)
            
        else:
            return super(ProcedureHandler, self).create(request, uuid, *args, **kwargs)

    def _read_by_uuid(self,request,uuid):
        """ Returns the procedure file instead of the verbose representation on 
            uuid GET requests 
        """
        model = getattr(self.__class__, 'model')
        obj =  model.objects.get(uuid=uuid)
        return open(obj.src.path).read()

@logged
class ProcedureGroupHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST', 'PUT')
    model = ProcedureGroup
    form = ProcedureGroupForm
    fields = (
        "uuid",
        "title",
        "description",
        "author",
        "procedures",
        "modified",
        "created",
        "voided",
    )
    def sync(self, request, uuid):
        proceduregroup = ProcedureGroup.objects.filter(uuid=uuid)
        if not proceduregroup:
            return fail('Procedure group not found', 404)
        else:
            proceduregroup = proceduregroup[0]
        if 'json' not in request.META.get('CONTENT_TYPE', ''):
            return fail('Unexpected content type', 400)
        server_procedures = proceduregroup.procedures.all()
        request_payload = ujson.loads(request.read())
        server_procedures = server_procedures.filter(voided=False).values('title').annotate(max_version=Max('version'))
        procedure_titles = [procedure['title'] for procedure in server_procedures]
        # Get procedures with a newer version
        procedures_to_update_clause = Q()
        request_procedures = request_payload.get('procedures', {})
        for server_procedure in server_procedures:
            request_procedure_version = request_procedures.get(server_procedure['title'], None)
            # If there is a version mismatch between the most recent non-voided procedure version on the server and client, return the most updated version to the client
            if not request_procedure_version or request_procedure_version != server_procedure['max_version']:
                where_clause = (Q(title=server_procedure['title']) & Q(version=server_procedure['max_version']))
                procedures_to_update_clause = procedures_to_update_clause | where_clause
        procedures_to_update = Procedure.objects.filter(procedures_to_update_clause) if len(procedures_to_update_clause) != 0 else []
        updated_procedures = [{'title': procedure.title, 'author': procedure.author, 'description': procedure.description, 'version': procedure.version, 'source_file_content': procedure.src.read()} for procedure in procedures_to_update]
        # Find procedures that don't exist in the group
        unknown_request_procedures = [request_procedure_title for request_procedure_title in list(request_procedures.keys()) if request_procedure_title not in procedure_titles]
        return_payload = {'updated_procedures': updated_procedures, 'unknown_procedures': unknown_request_procedures}
        return succeed(return_payload)
        
    def read(self, request, uuid=None, **kwargs):
        result_set = ProcedureGroup.objects.all()
        if uuid:
            result_set = result_set.filter(uuid=uuid)
        author_filter = request.GET.get('author', None)
        if author_filter:
            result_set = result_set.filter(author=author_filter)
        title_filter = request.GET.get('title', None)
        if title_filter:
            result_set = result_set.filter(title=title_filter)
        if not result_set and uuid:
            return fail('Could not find procedure group with given uuid')
        elif uuid:
            result_set = result_set[0]
        return succeed(result_set)
    def create(self,request, uuid=None, *args, **kwargs):
        if 'sync' == kwargs.get('op', None):
            if uuid:
                return self.sync(request, uuid)
            else:
                return fail('Not Found', 404)
        else:
            super(ProcedureGroupHandler, self).create(request, uuid, args, kwargs)
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

        
@logged
class SubjectHandler(DispatchingHandler):
    """ Handles subject requests. """
    allowed_methods = ('GET', 'POST','PUT')
    fields = (
        "uuid",
        "family_name",
        "given_name",
        "gender",
        "dob",
        "image",
        "system_id",
        ("location",("name","uuid")),
        "modified",
        "created",
        "voided",
    )
    model = Subject
    form = SubjectForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

class DocHandler(BaseHandler):
    """ Handles rest api documentation requests. """
    allowed_methods = ('GET',)
    documents = [EncounterHandler]
    
    #TODO fix this
    def read(self, request, *args, **kwargs):
        _handled = getattr(self.__class__, 'documents', [])
        return [ handler_uri_templates(x) for x in _handled]
        
# new stuff
@logged
class LocationHandler(DispatchingHandler):
    model = Location
    fields = (
        "name",
        "uuid",
        "code",
    )

class CompoundFormHandler(object):
    forms = {}
    """ A list of 2-tuples representing the names and forms on the page """
    allowed_methods = ('POST',)
    
    def create(request, *args, **kwargs):
        cleaned = {}
        for k,v in list(getattr(self.__class__, "forms", {}).items()):
            form = v(request.ITEMS[k])
            form.full_clean()
            cleaned[k] = form
            
    def __call__(self):
        pass

def intake_handler(request,*args,**kwargs):
    pass




