# -*- coding: utf-8 -*-
# Copyright (C) 2020-2022 by the Free Software Foundation, Inc.
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

from unittest.mock import Mock

from django.contrib.auth.models import User

from allauth.account.models import EmailAddress

from django_mailman3.lib.user import get_django_user
from django_mailman3.tests.utils import TestCase


class TestGetDjangUser(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'test@example.com', 'testPass')
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=True)
        EmailAddress.objects.create(
            user=self.user, email='secondemail@example.com', verified=True)
        EmailAddress.objects.create(
            user=self.user, email='thirdemail@example.com', verified=True)

    def test_get_user_with_email(self):
        # Test we can get the user from Member objects.
        for email in (
                'test@example.com', 'secondemail@example.com',
                'thirdemail@example.com'):
            member = Mock()
            member.address = Mock(email=email)
            user = get_django_user(member)
            self.assertEqual(user, self.user)

    def test_missing_user(self):
        # test that we don't raise exception when the user doesn't exist.
        member = Mock()
        member.address = Mock(email='example@example.com')
        self.assertIsNone(get_django_user(member))
