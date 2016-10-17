from allauth.socialaccount.models import SocialAccount
import requests
from allauth.socialaccount.models import SocialToken

def get_mutual_friends(user_id):
	GRAPH_API_VERSION = getattr(
		settings, 'SOCIALACCOUNT_PROVIDERS', {}
	).get('facebook', {}).get('VERSION', 'v2.4')

	GRAPH_API_URL = 'https://graph.facebook.com/' + GRAPH_API_VERSION
	# return GRAPH_API_URL + '/%s/picture?type=square&height=600&width=600&return_ssl_resources=1' % user_id
	return GRAPH_API_URL + '/{}?fields=context.fields%28mutual_friends%29'.format(user_id)



try:
	social_account = SocialAccount.objects.get(user=request.user)

except SocialAccount.DoesNotExist:
	social_account = None

if social_account:
	print social_account.uid
	token = SocialToken.objects.filter(account__user=request.user, account__provider='facebook')
	real_token = str(token[0])
	# 1143743712344887
	string_for_query = get_mutual_friends('1179863822034803')

	my_request = requests.get(
		string_for_query,
		params={
			'access_token': real_token
		}

	)
	print my_request.content

from django.conf import settings


