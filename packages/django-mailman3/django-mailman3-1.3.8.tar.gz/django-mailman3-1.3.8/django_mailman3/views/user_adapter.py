# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 by the Free Software Foundation, Inc.
#
# This file is part of Django-Mailman.
#
# Django-Mailman3 is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Django-Mailman3 is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Django-Mailman.  If not, see <http://www.gnu.org/licenses/>.


from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class DisableSignupAdapter(DefaultAccountAdapter):
    """Account adapter that disables signups.

    To use this, just set this in your settings.py::

        ACCOUNT_ADAPTER = \
            'django_mailman3.views.user_adapter.DisableSignupAdapter'
    """

    def is_open_for_signup(self, req):
        return False


class DisableSocialSignupAdapter(DefaultSocialAccountAdapter):
    """Social account adapter that disables signup.

    To use this, just set this in your settings.py::

         SOCIALACCOUNT_ADAPTER = \
             'django_mailman3.views.user_adapter.DisableSocialSignupAdapter'
    """

    def is_open_for_signup(self, req, socialaccount):
        return False
