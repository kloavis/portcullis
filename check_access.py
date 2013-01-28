# Create your views here.
from django.http import HttpResponse
from django.core import serializers
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.utils.http import urlquote

def check_access(request):

    if(request.user.username == ''):
        return HttpResponseRedirect("/portcullis/greeting/?next=%s" % urlquote(request.get_full_path()))

    t = loader.get_template('login.html');

    if(not request.user.is_active):
        c = Context({'user':request.user,'access_error':'User is not active'});
        return HttpResponse(t.render(c))

    return 0;
