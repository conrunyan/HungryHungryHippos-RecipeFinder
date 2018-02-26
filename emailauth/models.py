# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class EmailAuth(models.Model):
    '''Class contains email user authentication status'''

    usr_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_authenticated = models.BooleanField()
    authentication_id = models.CharField(max_length=None)
   
    def __str__(self):
        '''Returns a string with the email and authentication flag values'''
        return 'Email: {0} Authentication Status: {1}'.format(self.email, self.is_authenticated)
 
def makeEmailAuth(usr_id, is_auth):
    EmailAuth.objects.create(usr_id=id, is_authenticated=False, authentication_id=auth_id)
    ea = EmailAuth.objects.get(usr_id=id)
    print 'Email Auth model created',str(ea)

def makeUserAuthLink(usr_email):
    '''Function generates a sha256 version of the given email.given

    Will be used as the url/authentication key for a given user.
    '''
    cwd = os.getcwd()
    auth_url = 'hhhippo.tk/emailauth/activate/id='
    test_url = '10.10.10.102:8000/emailauth/activate/id='

    # check whether in staging, prod, or testing branch
    if re.search(r'.*staging.*', cwd) is None:
        auth_url = 'test.' + auth_url
    elif re.search(r'.*production.*', cwd) is None:
        # do nothing
        pass
    else:
        auth_url = test_url

    sha256_hash = hashlib.sha256()
    sha256_hash.update(usr_email)
    hash_key = sha256_hash.hexdigest()

    auth_url += hash_key

    return auth_url

  
