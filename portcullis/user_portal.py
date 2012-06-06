from models import DataStream, Permission
from django.http import HttpResponse
from django.template import Context, loader
from django.core.context_processors import csrf
from check_access import check_access

def user_streams(request):

    response = check_access(request)
    if(response):
        return response

    if request.method == 'GET':
        #Pull streams that are owned by this user.
        owned_streams = Permission.objects.filter(user = request.user, owner = True) 
        
        #Pull streams that are viewable by this useri.
        viewable_streams = Permission.objects.filter(user = request.user, read = True) 
        print viewable_streams

        #Pull any public streams as well
        public_streams = DataStream.objects.filter(is_public = True)


        t = loader.get_template('user_streams.html')
        c = Context({'user':request.user,'owned_streams':owned_streams, 'public_streams':public_streams,'viewable_streams':viewable_streams})
        c.update(csrf(request))
        return HttpResponse(t.render(c))


