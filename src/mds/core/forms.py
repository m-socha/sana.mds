'''

:Authors: Sana Dev Team
:Version: 2.0
'''
import logging
from datetime import datetime
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import *
from .widgets import *
from mds.core.extensions.forms import *

__all__ = ['ConceptForm', 'RelationshipForm', 'RelationshipCategoryForm', 
           'DeviceForm',
           'EncounterForm',
           'EventForm',
           'NotificationForm',
           'ObserverForm', 
           'ObservationForm', 
           'SubjectForm',
           'ProcedureForm',
           'SessionForm',
           ]

class SessionForm(forms.Form):
    """ Authentication Form """
    username = forms.CharField()
    password = forms.PasswordInput()

class ConceptForm(forms.ModelForm):
    """ A simple concept form 
    """
    class Meta:
        model = Concept
        fields = "__all__"

class RelationshipForm(forms.ModelForm):
    """ A simple concept relationship form 
    """
    class Meta:
        model = Relationship
        fields = "__all__"

class RelationshipCategoryForm(forms.ModelForm):
    """ A simple concept relationship category form 
    """
    class Meta:
        model = RelationshipCategory
        fields = "__all__"

class DeviceForm(forms.ModelForm):
    """ A simple Client form
    """
    class Meta:
        model = Device
        fields = "__all__"

class EncounterForm(forms.ModelForm):
    """ A simple encounter form.
    """
    class Meta:
        model = Encounter
        fields = "__all__"

class EventForm(forms.ModelForm):
    """ A simple event form
    """
    class Meta:
        model = Event
        fields = "__all__"

class NotificationForm(forms.ModelForm):
    """ Form for sending notifications """
    class Meta:
        model = Notification
        fields = "__all__"

class ObservationForm(forms.ModelForm):
    """ A simple observation form """
    class Meta:
        model = Observation
        fields = ('encounter', 'concept', 'node', 'value_text','value_complex')

class ObserverForm(forms.ModelForm):
    """ A simple observation form """
    class Meta:
        model = Observer
        fields = "__all__"

class ProcedureForm(forms.ModelForm):
    """ A simple procedure form
    """
    use_age = forms.BooleanField()
    
    class Meta:
        model = Procedure
        fields = "__all__"
     
class SubjectForm(forms.ModelForm):
    """ A simple patient form
    """
    class Meta:
        model = Subject
        fields = "__all__"
