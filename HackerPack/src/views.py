from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from notify.views import mark, delete

from models import UserProfile, UserProfileFilter, Team, TeamMember, Hackathon
from . import models
from .forms import SettingsForm, InviteForm, TeamForm
from .signals import accept_team, join_team


def index(request):
	if request.method == 'POST':
		# For removing a hackathon
		if 'removehackathonform' in request.POST:
			user = request.user
			removed_hackathon_id = request.POST.get("hackathon", "")
			removed_hackathon = Hackathon.objects.get(id=removed_hackathon_id)
			user.userprofile.hackathons.remove(removed_hackathon)

			responseobject = {
				'hackathon': str(removed_hackathon)
			}

			return JsonResponse(responseobject)

		# For adding user to hackathon
		elif 'goinghackathonform' in request.POST:
			user = request.user
			hackathon_id = request.POST.get("hackathon_id", "")
			hackathon = Hackathon.objects.get(id=hackathon_id)

			message = "You have already confirmed going to " + str(hackathon)
			print(message)

			if hackathon not in user.userprofile.hackathons.all():
				user.userprofile.hackathons.add(hackathon)
				message = "You have confirmed that you will be going to " + str(
					hackathon) + "!"

			responseobject = {
				'message': message
			}
			return JsonResponse(responseobject)

		# For removing a hackmate from team
		elif 'removehackmateform' in request.POST:
			removed_user = str(request.POST.get("remove_user", ""))
			removed_team = request.POST.get("remove_team", "")
			print(removed_team)

			removed_user_o = User.objects.get(username=removed_user)
			removed_team_o = Team.objects.get(id=removed_team)
			removed_member_o = TeamMember.objects.get(user=removed_user_o,
			                                          team=removed_team_o)
			removed_member_o.delete()

			responseobject = {
				'removed_user': removed_user_o.first_name,
				'removed_team': str(removed_team_o)
			}
			return JsonResponse(responseobject)

		# For messaging a team
		elif 'teamsendform' in request.POST:
			selected_user_team = str(request.POST.get("team", ""))
			teams_o = Team.objects.get(id=selected_user_team)
			members_set = teams_o.teammember_set.all()
			recipients_list = []

			for member in members_set:
				recipients_list.append(member.user.email)

			email_subject = "Meet your HackMates!"

			email_content = render_to_string(
				template_name='account/email/invite_teammates_to_chat.html',
				context={
					'sender_first_name': request.user.first_name,
					'team_name': teams_o
				}
			)

			send_mail(
				subject=email_subject,
				message="",
				html_message=email_content,
				from_email="hello@hackerpack.io",
				recipient_list=recipients_list
			)

			return JsonResponse({'the_team': str(teams_o)})

		# For forming a team
		elif 'teamform' in request.POST:
			team_form = TeamForm(data=request.POST)

			if team_form.is_valid():
				team_created = team_form.create_team(request.user)

				error = False

				if not team_created:
					error = True

				responseobject = {'error': error}

				return JsonResponse(data=responseobject)

		# For inviting people
		elif 'inviteform' in request.POST:

			invite_form = InviteForm(data=request.POST, prefix='invite')

			if invite_form.is_valid():
				invited = str(request.POST.get("invite-invited_user", ""))
				user_invited = User.objects.get(username=invited)
				name_invited = str(user_invited.first_name)
				team_selected = invite_form.invite(request, request.user,
				                                   invited)

				errormessage = ''
				error = False

				if isinstance(team_selected, unicode):
					error = True
					errormessage = team_selected
				else:
					join_team(request, invited, team_selected)

				responseobject = {
					'error': error,
					'errormessage': errormessage,
					'invited': name_invited
				}
				return JsonResponse(responseobject)

		# For accepting invitation
		else:
			team = request.POST.get('team', None)
			sender = request.POST.get('sender', None)
			user = request.user
			invited_user = User.objects.get(username=user)

			# Adding member to the team
			team_o = Team.objects.get(name=team)
			name = str(team_o.name + invited_user.username)

			# Only add if member is not already in team
			if (TeamMember.objects.filter(name=name).exists() == 0):
				invited_teammember = TeamMember(user=invited_user, team=team_o,
				                                name=name)
				hackathon_name = Hackathon.objects.get(title=team_o.hackathon)
				invited_user.userprofile.hackathons.add(hackathon_name)
				invited_teammember.save()
				accept_team(request, sender, team)

			# Change the notification settings
			mark(request)
			return (delete(request))

	else:
		hackathons = models.Hackathon.objects.order_by('start_date')

		if request.user.is_authenticated():

			f = UserProfileFilter(request.GET,
			                      queryset=UserProfile.objects.all())
			users = User.objects.filter(userprofile__in=f.qs).order_by('?')
			invite_form = InviteForm(user=request.user, prefix='invite')
			user_teams = request.user.teammember_set.all()
			# user_hackathons = request.user.userprofile.hackat

			context = {
				'title': 'Home',
				'users': users,
				'user_teams': user_teams,
				'hackathons': hackathons,
				'invite_form': invite_form,
				'team_form': TeamForm(),
				'filter': f,
				'count': users.count(),
			}
		else:
			users = User.objects.order_by('?')
			context = {
				'title': 'Home',
				'users': users,
				'hackathons': hackathons,
				'count': users.count(),
			}

		return render(request, 'home/index.html', context)


class CompanyView(TemplateView):
	template_name = 'team/index.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, self.get_context_data())

	def get_context_data(self, **kwargs):
		context = super(CompanyView, self).get_context_data(**kwargs)
		context['title'] = 'team'
		return context


@login_required
def profile(request):
	# Determine if this is an update to user info
	if request.method == 'POST':

		# Creates an empty form and and loads in data from the request.post
		form = SettingsForm(request.POST, request.FILES)

		# Verify if data inputted is usable
		if form.is_valid():
			user = request.user
			# Writes data in database
			form.update_profile(request, user)

			# Reloads the page with new user information
			return HttpResponseRedirect('/')

		profile = request.user.userprofile
		context = {
			'title': 'My Profile',
			'form': form,
			'profile': profile
		}
		return render(request, 'account/profile.html', context)

	else:

		profile = request.user.userprofile

		# Default information is shown
		settingForm = SettingsForm(
			initial={'about': profile.about,
			         'ideas': profile.ideas,
			         'frameworks': profile.frameworks
			         }
		)

		# print(profile.preference_tags)

		context = {
			'title': 'My Profile',
			'form': settingForm,
			'profile': profile
		}
		return render(request, 'account/profile.html', context)


@login_required
def hacker_teams(request, team_id):
	if request.method == "GET":
		user_team = Team.objects.get(id=team_id)
		print(user_team.members.all())

		context = {
			'team': user_team,
			'title': 'Team'
		}

		return render(request, 'home/hackteam.html', context)
