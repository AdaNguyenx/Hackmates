from django import forms
from django.core.files.images import get_image_dimensions
from django.core.validators import MinValueValidator, MaxValueValidator
from taggit.forms import TagField

from .models import UserProfile


class SignupForm(forms.Form):
	first_name = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
		label="",
		max_length=50,
	)

	last_name = forms.CharField(max_length=50, label='Enter your last name')

	age = forms.IntegerField(
		validators=[MinValueValidator(1), MaxValueValidator(100)]
	)

	# Save your profile
	def signup(self, request, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()


from .models import UserRoles, UserLanguage
from django.forms import Textarea


# Form for the user to change their name, about, city, school, etc.
class SettingsForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = [
			'email',
			'first_name',
			'last_name',
			'about',
			'school',
			'city',
			'studies',
			'avatar',
			'frameworks',
			'ideas'
		]
		widgets = {
			'frameworks': Textarea(attrs={'rows': 2}),
			'about': Textarea(attrs={'rows': 6}),
			'ideas': Textarea(attrs={'rows': 5})
		}

	roles = forms.ModelMultipleChoiceField(queryset=UserRoles.objects.all(),
	                                       widget=forms.CheckboxSelectMultiple,
	                                       required=False)

	languages = forms.ModelMultipleChoiceField(queryset=UserLanguage.objects.all(),
	                                           widget=forms.CheckboxSelectMultiple,
	                                           required=False)

	# preference_tags = TagField(
	# 	required=False
	# )

	def update_profile(self, request, user):
		# parsed_email = self.cleaned_data['first_name']
		parsed_first_name = self.cleaned_data['first_name']
		parsed_last_name = self.cleaned_data['last_name']

		# if parsed_email != "":
		# 	user.email = parsed_email

		if parsed_first_name != "":
			user.first_name = parsed_first_name

		if parsed_last_name != "":
			user.last_name = parsed_last_name

		user.save()

		# Assigning to variable to make readable
		profile = request.user.userprofile

		parsed_city = self.cleaned_data['city']
		parsed_school = self.cleaned_data['school']
		parsed_about = self.cleaned_data['about']
		parsed_ideas = self.cleaned_data['ideas']
		parsed_frameworks = self.cleaned_data['frameworks']

		if parsed_city != "":
			profile.city = parsed_city
		if parsed_school != "":
			profile.school = parsed_school
		if parsed_about != "":
			profile.about = parsed_about
		if parsed_ideas != "":
			profile.ideas = parsed_ideas
		if parsed_frameworks != "":
			profile.frameworks = parsed_frameworks

		parsed_roles = self.cleaned_data['roles']

		if parsed_roles is not None:
			profile.roles = parsed_roles

		parsed_languages = self.cleaned_data['languages']

		if parsed_roles is not None:
			profile.languages = parsed_languages

		parsed_avatar = self.clean_avatar()

		if parsed_avatar is not None:
			profile.avatar = parsed_avatar

		profile.save()

	def clean_avatar(self):
		avatar = self.cleaned_data['avatar']

		if avatar is not None:
			try:
				w, h = get_image_dimensions(avatar)
				# validate dimensions
				max_width = max_height = 1000

				if w > max_width or h > max_height:
					raise forms.ValidationError(
						u'Please use an image that is '
						'%s x %s pixels or smaller.' % (max_width, max_height))

				# validate content type
				main, sub = avatar.content_type.split('/')

				if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif',
				                                    'png']):
					raise forms.ValidationError(
						u'Please use a JPEG, '
						'GIF or PNG image.'
					)

				# validate file size
				if len(avatar) > (1000 * 1024):
					raise forms.ValidationError(
						u'Please use an image less than 1MB.')

			except AttributeError:
				print("ERROR")
				pass

				"""
				Handles case when we are updating the user profile
				and do not supply a new avatar
				"""

			return avatar


from django.core.exceptions import ValidationError


class DynamicMultipleChoiceField(forms.MultipleChoiceField):
	# The only thing we need to override here is the validate function.
	def validate(self, value):
		if self.required and not value:
			raise ValidationError(self.error_messages['required'])


from .models import Team, TeamMember, Hackathon
from django.contrib.auth.models import User


class InviteForm(forms.Form):
	teams = DynamicMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
	                                   choices=[])
	invited_user = forms.CharField(
		widget=forms.HiddenInput(attrs={'id': 'form-invited'}))

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		if self.user is not None:
			user_teams = [(o.name, o) for o in self.user.team_set.all()]
			self.base_fields['teams'].choices = user_teams
			super(InviteForm, self).__init__(*args, **kwargs)
		else:
			super(InviteForm, self).__init__(*args, **kwargs)

	def invite(self, request, user, invited):
		# Getting updated data
		team_selected = self.cleaned_data['teams']

		invited_user = User.objects.get(username=invited)

		errormessage = ''

		# Checking if teammember is already in team
		for team_index in team_selected:
			team_o = Team.objects.get(name=team_index)
			name = str(team_o.name + invited_user.username)
			if TeamMember.objects.filter(name=name).exists():
				if errormessage == '':
					errormessage = team_index
				else:
					errormessage += ', ' + team_index

		if errormessage == '':
			return team_selected
		else:
			return errormessage


class TeamForm(forms.Form):
	name = forms.CharField(max_length=32, required=True)
	description = forms.CharField(max_length=9001, required=False,
	                              initial="description")
	hackathon = forms.ModelChoiceField(queryset=Hackathon.objects.all(),
	                                   empty_label="")

	def create_team(self, user):
		parsed_name = self.cleaned_data['name']
		parsed_description = self.cleaned_data['description']
		parsed_hackathon = self.cleaned_data['hackathon']
		print(parsed_hackathon)

		hackathon = Hackathon.objects.get(title=str(parsed_hackathon))

		if Team.objects.filter(name=parsed_name).exists():
			return False
		else:
			# Create new team
			team = Team(
				name=parsed_name,
				description=parsed_description,
				hackathon=hackathon
			)
			team.save()

			# Create new teammember
			name = str(parsed_name + user.username)
			teammember = TeamMember(user=user, team=team, name=name)
			teammember.save()

			# Add user to the hackathon if user is not already in it
			if (user.userprofile.hackathons.filter(
				title=parsed_hackathon).exists() == 0):
				user.userprofile.hackathons.add(hackathon)

			return True
