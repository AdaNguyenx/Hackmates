import tempfile

import django_filters
import requests
from allauth.account.signals import user_signed_up
from django.conf import settings
from django.contrib.auth.models import User
from django.core import files
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager

from .utils import convert_keys_to_string_from_unicode


class Hackathon(models.Model):
	# Basic Info
	title = models.CharField(max_length=30)
	description = models.CharField(max_length=100)

	# Hackathon start and end
	start_date = models.DateField(default=now)
	end_date = models.DateField(default=now)

	# Location
	street = models.CharField(max_length=30)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length=30)

	# Any Personal URL
	website_url = models.URLField(max_length=50)

	# Length of a Hacking at a Hackathon
	length = models.IntegerField(default=24)

	hackathon_image = models.ImageField(
		default='images/users/default/default.png',
		blank=True
	)

	def __unicode__(self):
		return self.title


class Team(models.Model):
	name = models.CharField(
		max_length=64, unique=True, default='name',
		help_text="Enter a descriptive and unique name for your team (eg. HackPrinceton123)"
	)
	description = models.TextField(max_length=1024, default="a team")
	members = models.ManyToManyField(User, through='TeamMember')
	hackathon = models.ForeignKey(Hackathon, default='hackathon')

	def __unicode__(self):
		return self.name


class TeamMember(models.Model):
	user = models.ForeignKey(User, default='user')
	team = models.ForeignKey(Team, default='team')
	name = models.CharField(max_length=50, default='name', unique=True)

	# objects = TeamMemberManager()

	def __unicode__(self):
		return self.team.name + self.user.username

class UserLanguage(models.Model):
	language = models.CharField(max_length =100, default= "None")

	def __unicode__(self):
		return self.language

class UserRoles(models.Model):

	role = models.CharField(max_length =100, default= "None")

	def __unicode__(self):
		return self.role

class UserProfile(models.Model):
	email = models.EmailField(max_length=200, blank=True)
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50, blank=True)

	about = models.TextField(max_length=500, default='I am a hackmate!', blank=True)
	frameworks = models.TextField(max_length=500, default='None', blank=True)
	ideas = models.TextField(max_length=500, default='None yet :(', blank=True,
	                         help_text='Tell us your hackathon ideas!')

	city = models.CharField(
		max_length=32, default='HackerPack Land', blank=True
	)

	user = models.OneToOneField(User, unique=True)
	hackathons = models.ManyToManyField(Hackathon, blank=True)

	avatar = models.ImageField(
		# Error below I need to fix
		default='images/users/default/default.png',
		blank=True
	)

	school = models.CharField(max_length=50, default='HackerPack', blank=True)

	studies = models.CharField(max_length=32, default='Hacking', blank=True)

	# preference_tags = TaggableManager()


	roles = models.ManyToManyField(UserRoles, blank=True)
	languages = models.ManyToManyField(UserLanguage, blank=True)

	def __unicode__(self):
		return str(self.user.username)


def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


def get_image_url(user_id):
	GRAPH_API_VERSION = getattr(
		settings, 'SOCIALACCOUNT_PROVIDERS', {}
	).get('facebook', {}).get('VERSION', 'v2.4')

	GRAPH_API_URL = 'https://graph.facebook.com/' + GRAPH_API_VERSION
	return GRAPH_API_URL + '/%s/picture?type=square&height=600&width=600&return_ssl_resources=1' % user_id


@receiver(user_signed_up)
def user_signed_up_(request, user, sociallogin=None, **kwargs):
	# Extract first / last names from social nets and store on User record
	if sociallogin:
		if sociallogin.account.provider == 'facebook':
			profile = user.userprofile

			social_login_info = convert_keys_to_string_from_unicode(
				sociallogin.account.extra_data
			)

			print social_login_info

			# Obtaining User Information
			profile.first_name = social_login_info['first_name']
			profile.last_name = social_login_info['last_name']

			try:
				profile.city = social_login_info['location']['name']
			except KeyError as e:
				pass

			try:
				profile.about = social_login_info['bio']
			except KeyError as e:
				pass

			try:
				# Querying Education Information
				educations = social_login_info['education']

				profile.school = educations[-1]['school']['name']
				profile.studies = educations[-1]['concentration'][0]['name']

			except KeyError as e:
				pass

			image_url = get_image_url(str(social_login_info['id']))
			request = requests.get(image_url, stream=True)

			# Was the request ok
			# Nope, error handling, skip file etc etc etc
			if request.status_code != requests.codes.ok:
				pass

			# Create a temporary file
			lf = tempfile.NamedTemporaryFile()

			# Read the streamed image in sections
			# If no more file then stop
			for block in request.iter_content(1024 * 8):
				if not block:
					break
				lf.write(block)  # Write image block to temporary file

			profile.avatar.save(user.username, files.File(lf))

			profile.save()



from django.forms import SelectMultiple
class UserProfileFilter(django_filters.FilterSet):
	class Meta:
		model = UserProfile
		fields = ['hackathons__title', 'school', 'roles__role', 'languages__language']

	hackathons__title = django_filters.ModelMultipleChoiceFilter(
		queryset=Hackathon.objects.all(), label='Hackathons', help_text=''
	)

	languages__language = django_filters.ModelMultipleChoiceFilter(
		queryset=UserLanguage.objects.all(), label='Languages', help_text=''
	)

	roles__role = django_filters.ModelMultipleChoiceFilter(
		queryset=UserRoles.objects.all(), label='Roles',
		help_text='Select role(s) you are looking for your team',
		# widget= SelectMultiple(attrs={'size':8})
	)

	school = django_filters.CharFilter(lookup_expr='icontains', help_text='')


