from src.models import UserLanguage

LANGUAGES = [
	'C',
	'C#',
	'C++',
	'CSS',
	'HTML',
	'Java',
	'Javascript',
	'Objective C',
	'PHP',
	'Python',
	'Ruby',
	'Swift',
	'None'
]

for LANGUAGE in LANGUAGES:
	UserLanguage.objects.create(language=LANGUAGE)
