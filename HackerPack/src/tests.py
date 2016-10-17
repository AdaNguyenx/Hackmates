from django.test import TestCase

from .forms import SettingsForm
from .models import Hackathon, User, Team, TeamMember, UserProfile

class ProfileViewTest(TestCase):
	def setUp(self):
		RANDOM_NUMBER_NOT_ONE = 20

		test_user_1 = User.objects.create(
			username='test_user_1',
			first_name='Alexa',
			last_name='Boombox',
		)

		test_user_profile = UserProfile.objects.create(
			user_id=RANDOM_NUMBER_NOT_ONE,
			# user=test_user_1,
			first_name=test_user_1.first_name,
			last_name=test_user_1.last_name,
		)

	def test_empty_form(self):
		form_data = {}
		profile_form = SettingsForm(data=form_data)

		# Should we prevent user from submitting an empty form?

		self.assertTrue(profile_form.is_valid())

	def test_name_form(self):
		form_data = {
			'first_name': 'Jaime',
			'last_name': 'Orellana'
		}
		profile_form = SettingsForm(data=form_data)

		self.assertTrue(profile_form.is_valid())

		test_user_1 = User.objects.get(username='test_user_1')

		test_user_1.first_name = profile_form.cleaned_data['first_name']
		test_user_1.last_name = profile_form.cleaned_data['last_name']

		test_user_1.save()

		self.assertEqual(test_user_1.first_name, 'Jaime')
		self.assertEqual(test_user_1.last_name, 'Orellana')


# Tests the TeamView with a created a team
class TeamView(TestCase):
	def setUp(self):
		test_user_1 = User.objects.create(
			username='test_user_1',
			first_name='Alexa',
			last_name='Boombox'
		)

		test_user_2 = User.objects.create(
			username='test_user_2',
			first_name='Monique',
			last_name='Brooks'
		)

		test_hackathan = Hackathon.objects.create(
			title='Test Hackathon',
			description='Test Description',
			street='Test Street',
			city='Test City',
			state='Test State',
			website_url="http://google.com"
		)

		test_team = Team.objects.create(
			name='Test Team',
			description='Test Description',
			hackathon=test_hackathan
		)

		TeamMember.objects.create(
			name='Hoccus', user=test_user_1, team=test_team
		)

		TeamMember.objects.create(
			name='Poccus', user=test_user_2, team=test_team
		)

	# def user_must_be_logged_in(self):
	# 	response = self.client.get('our-teams')

	def test_removing_team_member(self):
		test_user_1 = TeamMember.objects.get(name='Hoccus')
		test_user_2 = TeamMember.objects.get(name='Poccus')

		self.assertEqual(test_user_1.team, test_user_2.team)

		test_user_1.delete()

		self.assertEqual(test_user_2.team.members.count(), 1)

		test_user_2.delete()

		# Verify team no longer exists
		self.assertEqual(Team.objects.count(), 0)
