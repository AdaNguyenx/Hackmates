import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '5ftn)xd^s7cv4lem2dvy3z2)0_203bu-=ekf%vnfwuk__^eaqq'

DEBUG = False

# When in production mode, these need to be defined

ALLOWED_HOSTS = [
	'.localhost',
	'127.0.0.1',
	'hackmates.io',
]

INSTALLED_APPS = [
	# Personal Apps
	'src',

	# Django Default Apps
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	# Local package req. for all-auth
	'django.contrib.sites',

	# Remote packages

	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.facebook',
	# 'allauth.socialaccount.providers.github',

	# Production
	'storages',

	# Bootstrap Form Formatter/Cleaner
	'bootstrapform',

	# Dynamic Tagging
	'taggit',

	# Filtering
	'django_filters',

	# Notification
	'notify',

	# Parsing dictionary arguments via django templates
	'jsonify',

	'multiselectfield'

]

MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HackerPack.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, 'templates'),
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

# Part of the DjangoAllAuth application's settings
# When beginning production, uncomment this line
# By default it's set to "optional"


# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_SIGNUP_FORM_CLASS = 'src.forms.SignupForm'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_LOGOUT_ON_GET = True  # Logout in one click

WSGI_APPLICATION = 'HackerPack.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'HOST': os.environ['RDS_HOSTNAME'],
			'NAME': os.environ['RDS_DB_NAME'],
			'USER': os.environ['RDS_USERNAME'],
			'PASSWORD': os.environ['RDS_PASSWORD'],
			'PORT': os.environ['RDS_PORT'],
		}
	}
else:
	# DATABASES = {
	# 	'default': {
	# 		'ENGINE': 'django.db.backends.sqlite3',
	# 		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	# 	}
	# }

	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'HOST': 'hack-mates.cdfklbzzmvda.us-east-1.rds.amazonaws.com',
			'NAME': 'hack_mates',
			'USER': 'supersaiyan',
			'PASSWORD': 'hackerpackislove',
			'PORT': '5432',
		}
	}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

AUTHENTICATION_BACKENDS = (
	# Needed to login by username in Django admin, regardless of `allauth`
	'django.contrib.auth.backends.ModelBackend',

	# `allauth` specific authentication methods, such as login by e-mail
	'allauth.account.auth_backends.AuthenticationBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Required by all-auth
SITE_ID = 4

SOCIALACCOUNT_PROVIDERS = {
	'facebook': {
		'METHOD': 'oauth2',
		'SCOPE': [
			'email',
			'public_profile',
			'user_friends',
			'user_education_history',
			'user_location',
			'user_about_me'
		],
		'AUTH_PARAMS': {},
		'FIELDS':
			[
				'id',
				'email',
				'name',
				'first_name',
				'last_name',
				'verified',
				'locale',
				'timezone',
				'link',
				'gender',
				'updated_time',
				'picture',

				# Uses 'user_education_history'
				'education',

				# Uses 'user_location'
				'location',

				# Uses 'user_about_me'
				'bio',

				'context',
				# 'about',

			],
		'EXCHANGE_TOKEN': True,
		'LOCALE_FUNC': lambda request: 'en_US',
		'VERIFIED_EMAIL': True,
		'VERSION': 'v2.4'
	}
}

STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "www", "media")

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'static')
]

# Prints the information to the console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Actually sends it to the server
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'jaime5'
EMAIL_HOST_PASSWORD = 'hackerpackislove1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = "hello@hackerpack.io"

# Production:
if not DEBUG:

	# Informs browser that caching of page is possible
	AWS_HEADERS = {
		'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
		'Cache-Control': 'max-age=94608000',
	}

	AWS_STORAGE_BUCKET_NAME = 'hack-mates'
	AWS_ACCESS_KEY_ID = 'AKIAIRHX2BPC5U4S6ODA'
	AWS_SECRET_ACCESS_KEY = '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'

	# Tell django-storages that when coming up with the URL for an item in S3 storage
	# NOTE: Keep it simple - just use this domain plus the path.
	# NOTE: If this isn't set, things get complicated

	# Control how the `static` template tag from `staticfiles` gets expanded
	AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

	STATICFILES_LOCATION = 'static'
	STATICFILES_STORAGE = 'custom_storages.StaticStorage'
	STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

	# This is used by the `static` template tag from `static`
	# In anycase, this refers directly to STATIC_URL, hence safe to always set

	# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

	# Tell the staticfiles app to use S3Boto storage when writing the collected
	# static files (when you run `collectstatic`)
	# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

	MEDIAFILES_LOCATION = 'media'
	MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
	DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

# Development
else:

	STATIC_URL = '/static/'
	MEDIA_URL = '/media/'

	STATICFILES_FINDERS = (
		'django.contrib.staticfiles.finders.FileSystemFinder',
		'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	)
