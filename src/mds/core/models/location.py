''' sana.core.models.location

:author: Sana Development Team
:version: 2.0
:copyright: Sana 2012, released under BSD New License(http://sana.mit.edu/license)
'''

from django.db import models
from mds.api.utils import make_uuid
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Location(models.Model):
    
    class Meta:
        app_label = "core"
        
    uuid = models.SlugField(max_length=36, unique=True, default=make_uuid, editable=False)
    """ A universally unique identifier """
    
    name = models.CharField(max_length=255)
    """A label for identifying the location"""
    
    code = models.IntegerField(blank=True)
    
    def __str__(self):
        return '%s - %s' % (self.code,self.name)
