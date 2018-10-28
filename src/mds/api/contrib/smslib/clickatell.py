'''
Created on Aug 11, 2012

:author: Sana Development Team
:version: 2.0
'''
try:
    import json as simplejson
except ImportError as e:
    import simplejson
    
import logging
import urllib.request, urllib.parse, urllib.error

from django.conf import settings

def send_clickatell_notification(message_body, phoneId,formatter=None):
    return ClickatellOpener().open(message_body, phoneId,formatter=formatter)

class ClickatellOpener:
    
    def __init__(self):
        pass
    

    def open(self, n, phoneId, formatter=None):
        """Sends an SMS message to Clickatell http interface
            
        See Clickatell API documentation for full details. 
        
        Clickatell params
            user 
                Clickatell account user name
            password
                Clickatell account password
            api_id
                see Clickatell documentation
            to
                Recipient telephone number
            text
                Message Body
            
        Clickatell url: http://api.clickatell.com/http/sendmsg?params
        
        Parameters:
            message_body
                Message body
            phoneId
                Recipient
        """
        result = False
        try:
            messages = formatter(n) if formatter else n
            for message in messages:
    
                params = urllib.parse.urlencode({
                        'user': settings.CLICKATELL_USER,
                        'password': settings.CLICKATELL_PASSWORD,
                        'api_id': settings.CLICKATELL_API,
                        'to': phoneId,
                        'text': message
                        })
    
                logging.info("Sending clickatell notification %s to %s" %
                             (message, phoneId))
                response = urllib.request.urlopen(settings.CLICKATELL_URI % params).read()
                logging.info("Clickatell response: %s" % response)
                result = True
        except Exception as e:
            logging.error("Couldn't submit Clickatell notification for %s: %s" % (phoneId, e))
        return result
