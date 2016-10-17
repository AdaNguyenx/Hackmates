from django.conf.urls import url
from . import views
from .views import CompanyView

app_name = 'src'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'ourteam/$', CompanyView.as_view()),
	url(r'^accounts/profile/$', views.profile, name='profile'),
	url(r'hack-teams/(?P<team_id>[0-9]+)/$', views.hacker_teams, name = 'hacker_teams')
]
