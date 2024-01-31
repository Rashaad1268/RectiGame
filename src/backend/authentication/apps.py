from django.apps import AppConfig
from django.shortcuts import render

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        from . import signals
