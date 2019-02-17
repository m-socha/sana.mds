from django import forms

from .models import *

__all__ = [ 'EncounterTaskForm',
            'ObservationTaskForm']

class EncounterTaskForm(forms.ModelForm):
    class Meta:
        model = EncounterTask
        fields = "__all__"

class ObservationTaskForm(forms.ModelForm):
    class Meta:
        model = ObservationTask
        fields = "__all__"
