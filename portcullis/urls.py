from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'portcullis.views',
    url(r'^$', 'index.index', name='portcullis-index'),
    url(r'^login/$', 'login.user_login', name='portcullis-login'),
    url(r'^logout/$', 'login.logout', name='portcullis-logout'),
    url(r'^passwordForm/$', 'login.passwordForm', name='portcullis-passwordForm'),
    url(r'^changePassword/$', 'login.changePassword', name='portcullis-changePassword'),
    url(r'^side_pane/$', 'side_pane.skeleton', name='side_pane-skeleton'),
    url(r'^streams/$', 'side_pane.streams', name='side_pane-streams'),
    url(r'^(?P<content>savedView)/(?P<content_id>.+)/$', 'index.index', name='portcullis-saved-view'),
    url(r'^createSavedView/$', 'savedView.createSavedView', name='portcullis-saveView'),
    url(r'^model_editor/(?P<model_name>.+)/$', 'crud.model_grid', name='portcullis-model-editor')
)


