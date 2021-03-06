#System Imports
from django.http import HttpResponse
from django.template import Context, RequestContext, loader
from collections import OrderedDict

#Local Imports
from portcullis.models import DataStream
from check_access import check_access

def skeleton(request):
    '''
    Render the side_pane skeleton.  The other stuff will be loaded in later with ajax.
    '''

    user = check_access(request)
    logged_in = True
    if user is None or isinstance(user, HttpResponse):
        logged_in = False


    t = loader.get_template('side_pane.html')
    c = RequestContext(request, {
            'streams': streams(request).content,
            'logged_in': logged_in
            })
    return HttpResponse(t.render(c), mimetype='text/html')

def streams(request):
    '''
    Grab all relevent streams to display as checkboxes in the user portal.  We make sure to remove any duplicate streams from each various section.
    Presedence is given to owner, then to readable, then to public for the duplicate removal.
    '''

    user = check_access(request)

    if isinstance(user, HttpResponse):
        return user

    t_subtree = loader.get_template('stream_subtree.html')

    #Only get owned and viewable streams if we have a logged in User
    owned_streams = []
    viewable_streams = []
    owned_subtree = None
    viewable_subtree = None
    if user is not None:
        #Pull streams that are owned by this user.
        owned_streams = DataStream.objects.filter(owner = user)
        c_dict = stream_tree_top(owned_streams)
        c_dict.update({'group':'owned'})
        owned_subtree = t_subtree.render(Context(c_dict))

        #Pull streams that are viewable by this user.
        viewable_streams = DataStream.objects.get_viewable(user).exclude(id__in=owned_streams).distinct()
        c_dict = stream_tree_top(viewable_streams)
        c_dict.update({'group':'viewable'})
        viewable_subtree = t_subtree.render(Context(c_dict))

    #Pull any public streams as well
    public_streams = DataStream.objects.filter(is_public = True).exclude(id__in=viewable_streams).exclude(id__in=owned_streams).distinct()
    c_dict = stream_tree_top(public_streams)
    c_dict.update({'group':'public'})
    public_subtree = t_subtree.render(Context(c_dict))

    t_streams = loader.get_template('user_streams.html')
    c_streams = RequestContext(request, {
            'user':request.user,
            'owned_streams': owned_streams,
            'viewable_streams': viewable_streams,
            'public_streams': public_streams,
            'owned_subtree': owned_subtree,
            'public_subtree': public_subtree,
            'viewable_subtree': viewable_subtree
            })
    t_controls = loader.get_template('graph_controls.html')
    c_controls = RequestContext(request)
    
    return HttpResponse(t_controls.render(c_controls) + t_streams.render(c_streams), mimetype='text/html')

def stream_tree_top(streams):
    '''
    ' This function should create the top level tree structure for the datastreams, and return it as a dictionary.
    ' Only the keys should really be necessary, though.
    '
    ' Keyword Args:
    '    streams - An iterable of datastreams.
    '
    ' Returns:
    '    A dictionary containing the top level of the tree as strings.  The values are True for nodes, and
    '    False for leaves.
    '''
    nodes = {}
    leaves = {}
    for s in streams:
        # Assume for now that names are unique.
        # TODO: Validate (in save/models, etc.) that no 2 objects can have names such that name and name::other
        #  exist.
        spart = s.name.partition('|')
        if spart[2] != '':
            if spart[0] not in nodes:
                nodes[spart[0]] = None
        else:
            leaves[spart[0]] = s.id

    nodes = OrderedDict(sorted(nodes.iteritems(), key = lambda t: t[0]))
    leaves = OrderedDict(sorted(leaves.iteritems(), key = lambda t: t[0]))
    return {'nodes': nodes, 'leaves': leaves}



