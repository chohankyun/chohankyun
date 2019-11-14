# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions

from chohankyun import settings


class EmailMixin:
    def get_extras(self):
        """Override this method to add extra options"""
        return {}

    @staticmethod
    def _validate_email(email):
        user = get_user_model().objects.filter(email=email).first()

        if not user:
            msg = _('E-mail address matching query does not exist.')
            raise exceptions.ValidationError(msg)

        return user

    def send_email(self, subject_template_name, email_template_name):
        request = self.context.get('request')
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        user = self.validated_data['user']

        opt = {
            'domain': domain,
            'site_name': site_name,
            'user': user,
            'username': user.username,
            'protocol': 'https' if request.is_secure() else 'http',
        }

        opt.update(self.get_extras())

        subject = loader.render_to_string(subject_template_name, opt)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, opt)
        email_message = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
        email_message.send()
