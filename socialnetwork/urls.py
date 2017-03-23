from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from socialnetwork import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add-post$', views.add_post, name="add-post"),
    url(r'^del-post/(?P<post_id>\d+)$', views.del_post, name="del-post"),
    url(r'^show-profile/(?P<post_user>\w+)$', views.show_profile, name="show-profile"),
    url(r'^edit-profile$', views.edit_profile, name="edit-profile"),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name="logout"),
    url(r'^register$', views.register, name="register"),
    url(r'^picture/(?P<curr_user>\w+)$', views.get_picture, name='picture'),
    url(r'^get-list-json$', views.get_list_json, name="get-list-json"),
    url(r'^add-comment/(?P<post_id>\d+)$', views.add_comment, name="add-comment"),

    url(r'^add-post-json$', views.add_post_json, name="add-post-json"),
    url(r'^add-comment-json/(?P<post_id>\d+)$', views.add_comment_json, name="add-comment-json"),
    url(r'^del-post-json/(?P<post_id>\d+)$', views.del_post_json, name="del-post-json"),

    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        views.confirm_registration, name='confirm'),
]
