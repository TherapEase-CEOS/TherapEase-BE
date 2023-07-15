from .base import *  # noqa

DEBUG = False
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': env('DATABASE_NAME'),
#        'USER': env('DATABASE_USER'),
#        'PASSWORD': env('DATABASE_PASSWORD'),
#        'HOST': env('DATABASE_HOST'),
#        'PORT': env('DATABASE_PORT'),
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'therapease',
        'USER': 'admin',
        'PASSWORD': 'therapease',
        'HOST': 'therapease-mysql.c81tznyca4ah.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS':{
            'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

