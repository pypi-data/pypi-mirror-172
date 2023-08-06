# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2022 by the Free Software Foundation, Inc.
#
# This file is part of Django-Mailman.
#
# Django-Mailman is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Django-Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Django-Mailman.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aurelien Bompard <abompard@fedoraproject.org>
#


from unittest.mock import Mock, call, patch

from django.contrib.auth.models import User

from allauth.account.models import EmailAddress
from allauth.account.signals import (
    email_confirmed, email_removed, user_logged_in, user_signed_up)
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.signals import social_account_added

from django_mailman3.models import Profile
from django_mailman3.signals import user_subscribed, user_unsubscribed
from django_mailman3.tests.utils import TestCase


class SignalsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'test@example.com', 'testPass')

    def test_user_logged_in(self):
        Profile.objects.get(user=self.user).delete()
        with patch('django_mailman3.signals.sync_email_addresses') as sea:
            user_logged_in.send(sender=User, user=self.user)
        self.assertEqual(sea.call_args_list, [call(self.user)])
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_user_signed_up(self):
        Profile.objects.get(user=self.user).delete()
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=True)
        EmailAddress.objects.create(
            user=self.user, email='another@example.com', verified=False)
        with patch('django_mailman3.signals.add_address_to_mailman_user') \
                as aatmu:
            user_signed_up.send(sender=User, user=self.user)
        self.assertEqual(
            aatmu.call_args_list, [call(self.user, self.user.email)])
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_email_removed(self):
        address = EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=True)
        mm_user = Mock()
        with patch('django_mailman3.signals.get_mailman_user') as gmu:
            gmu.return_value = mm_user
            email_removed.send(
                sender=User, user=self.user, email_address=address)
        self.assertEqual(mm_user.addresses.remove.call_args_list,
                         [call(self.user.email)])

    def test_email_removed_no_mailman_user(self):
        address = EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=True)
        with patch('django_mailman3.signals.get_mailman_user') as gmu:
            gmu.return_value = None
            email_removed.send(
                sender=User, user=self.user, email_address=address)

    def test_email_confirmed(self):
        address = EmailAddress.objects.create(
            user=self.user, email=self.user.email, verified=True)
        with patch('django_mailman3.signals.add_address_to_mailman_user') \
                as aatmu:
            email_confirmed.send(sender=EmailAddress, email_address=address)
        self.assertEqual(
            aatmu.call_args_list, [call(self.user, self.user.email)])

    def test_social_account_added(self):
        verified = EmailAddress(
            email='verified@example.com', verified=True)
        unverified = EmailAddress(
            email='unverified@example.com', verified=False)
        sociallogin = SocialLogin(
            user=self.user, email_addresses=[verified, unverified])
        with patch('django_mailman3.signals.add_address_to_mailman_user') \
                as aatmu:
            social_account_added.send(sender=User, sociallogin=sociallogin)
        self.assertEqual(
            aatmu.call_args_list, [call(self.user, 'verified@example.com')])
        self.assertEqual(
            [e.user for e in EmailAddress.objects.all()],
            [self.user, self.user])

    def test_user_subscribed(self):
        with patch('django_mailman3.signals.get_subscriptions') as gs:
            user_subscribed.send(
                sender="Postorius", user_email="test@example.com")
            self.assertEqual(gs.call_count, 1)
            user_unsubscribed.send(
                sender="Postorius", user_email="test@example.com")
            self.assertEqual(gs.call_count, 2)

    def test_user_subscribed_secondary_address(self):
        EmailAddress.objects.create(
            user=self.user, email="test-2@example.com", verified=True)
        with patch('django_mailman3.signals.get_subscriptions') as gs:
            user_subscribed.send(
                sender="Postorius", user_email="test-2@example.com")
            self.assertEqual(gs.call_count, 1)
            user_unsubscribed.send(
                sender="Postorius", user_email="test-2@example.com")
            self.assertEqual(gs.call_count, 2)

    def test_create_profile(self):
        # Test that when a user is saved, we create a Profile if one doesn't
        # exist for the User. Also, we update the display name for the user and
        # their all addresses.
        mm_user = Mock()
        mm_user.display_name = None
        # Mock user has two addresses.
        mm_user.addresses = [Mock(), Mock()]

        with patch('django_mailman3.signals.get_mailman_user') as gmu:
            gmu.return_value = mm_user
            user = User.objects.create_user(
                'myuser', 'testing@example.com', 'testPass')
            # Initially, the name of user is null, so we don't update the
            # display_name in Core.
            gmu.assert_not_called()
            # Now lets update the name of the user and see if it is reflected.
            user.first_name = 'Anne'
            user.last_name = 'Person'
            user.save()
            # Assert that the mock user was fetched and that the display name
            # was set.
            gmu.assert_called_once_with(user)
            mm_user.save.assert_called_once()
            self.assertEqual(mm_user.display_name, 'Anne Person')
            for addr in mm_user.addresses:
                self.assertEqual(addr.display_name, 'Anne Person')
                addr.save.assert_called_once()

    def test_create_profile_one_name(self):
        # Same as test_create_profile but tests that first_name only has no
        # trailing space.
        mm_user = Mock()
        mm_user.display_name = None
        # Mock user has two addresses.
        mm_user.addresses = [Mock(), Mock()]

        with patch('django_mailman3.signals.get_mailman_user') as gmu:
            gmu.return_value = mm_user
            user = User.objects.create_user(
                'myuser', 'testing@example.com', 'testPass')
            # Initially, the name of user is null, so we don't update the
            # display_name in Core.
            gmu.assert_not_called()
            # Now lets update the name of the user and see if it is reflected.
            user.first_name = 'Anne'
            # user.last_name = 'Person'
            user.save()
            # Assert that the mock user was fetched and that the display name
            # was set.
            gmu.assert_called_once_with(user)
            mm_user.save.assert_called_once()
            self.assertEqual(mm_user.display_name, 'Anne')
            for addr in mm_user.addresses:
                self.assertEqual(addr.display_name, 'Anne')
                addr.save.assert_called_once()

    def test_create_profile_one_address_not_updated(self):
        # Similar to test_create_profile but tests that address.display_name
        # not updated if not changed.
        mm_user = Mock()
        mm_user.display_name = None
        # Mock user has two addresses.
        mm_user.addresses = [Mock(), Mock()]

        with patch('django_mailman3.signals.get_mailman_user') as gmu:
            gmu.return_value = mm_user
            user = User.objects.create_user(
                'myuser', 'testing@example.com', 'testPass')
            # Initially, the name of user is null, so we don't update the
            # display_name in Core.
            gmu.assert_not_called()
            # Now lets update the name of the user and see if it is reflected.
            user.first_name = 'Anne'
            user.last_name = 'Person'
            user.save()
            # Assert that the mock user was fetched and that the display name
            # was set.
            gmu.assert_called_once_with(user)
            mm_user.save.assert_called_once()
            self.assertEqual(mm_user.display_name, 'Anne Person')
            for addr in mm_user.addresses:
                self.assertEqual(addr.display_name, 'Anne Person')
                addr.save.assert_called_once()
            # Set second address display_name to new name.
            mm_user.addresses[1].display_name = 'Ann Person'
            # Reset the mocks and update the user.
            for addr in mm_user.addresses:
                addr.reset_mock()
            user.first_name = 'Ann'
            user.save()
            self.assertEqual(mm_user.display_name, 'Ann Person')
            self.assertEqual(mm_user.addresses[0].display_name, 'Ann Person')
            mm_user.addresses[0].save.assert_called_once()
            self.assertEqual(mm_user.addresses[1].display_name, 'Ann Person')
            mm_user.addresses[1].save.assert_not_called()
