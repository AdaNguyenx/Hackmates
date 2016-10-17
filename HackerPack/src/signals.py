from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from notify.signals import notify

from .models import Team


# Inviting a team member
def join_team(request, invited, team_selected):
	user = User.objects.get(username=invited)

	# Insert Process of Following
	for team in team_selected:
		invite_verb = "is inviting you to join their team "

		team_o = Team.objects.get(name=team)

		team_url = '/hack-teams/' + str(team_o.id)

		notify.send(
			request.user,
			recipient=user,
			actor=request.user,
			verb=invite_verb,
			nf_type='invite',
			description=str(team),
			target=team_o,
			actor_url="",
			target_url=team_url
		)

		# notifies a hackmates member that they've been invited to said team
		email_subject = "You've been invited to a Team!"
		email_message = render_to_string(
			template_name='account/email/invited_to_team_notification.html',
			context={
				'team_name': team,
				'inviter_first_name': request.user.first_name,
				'inviter_last_name': request.user.last_name
			}
		)
		email_receiver = [user.email]

		send_mail(
			subject=email_subject,
			message="",
			html_message=email_message,
			from_email='hello@hackerpack.io',
			recipient_list=email_receiver,
			fail_silently=True
		)


# When someone has accepted the request
def accept_team(request, receive, team):
	recipient = User.objects.get(username=receive)
	verb = str(" has accepted your request to join " + str(team))
	# actor_name = str(request.user.first_name) + " " + str(request.user.last_name)


	notify.send(
		request.user,
		recipient=recipient,
		actor=request.user,
		nf_type='accept',
		verb=verb,
		description=str(team)
	)


	# sending email to all teammates that a new user has joined their team
	email_receiver = []
	email_subject = "You have a new teammate!"
	email_message = render_to_string(
		template_name='account/email/new_team_member_notification.html',
		context={
			'team_name': team,
			'invitee_first_name': recipient.first_name,
			'invitee_last_name': recipient.last_name,
			'invitee_username': recipient.username
		}
	)

	try:
		team_object = Team.objects.get(name=team)

		for member in team_object.teammember_set.all():

			mail = member.user.email
			# Makes sure that the email does exist
			# Need to make so that the new team member doesn't get the
			# email saying "new team member"
			if mail is not None and request.user.email != mail:
				email_receiver.append(mail)

	except Team.DoesNotExist:
		print("No team exists")

	send_mail(
		subject=email_subject,
		message="",
		html_message=email_message,
		from_email='hello@hackerpack.io',
		recipient_list=email_receiver,
		fail_silently=True
	)
