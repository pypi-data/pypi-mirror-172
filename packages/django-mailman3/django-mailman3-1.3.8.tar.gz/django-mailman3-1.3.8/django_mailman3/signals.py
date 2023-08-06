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


import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from allauth.account.models import EmailAddress
from allauth.account.signals import (
    email_changed, email_confirmed, email_removed,
    user_logged_in, user_signed_up)
from allauth.socialaccount.signals import social_account_added

from django_mailman3.lib.mailman import (
    add_address_to_mailman_user, get_mailman_user, get_subscriptions,
    sync_email_addresses, update_preferred_address)
from django_mailman3.models import Profile


logger = logging.getLogger(__name__)

# Fields for settings.AUTH_USER_MODEL. These are for the default Django's
# contrib.auth.User model object.
FIELD_FIRST_NAME = 'first_name'
FIELD_LAST_NAME = 'last_name'

#
# Defined signals
#
domain_created = Signal()
domain_deleted = Signal()
mailinglist_created = Signal()
mailinglist_modified = Signal()
mailinglist_deleted = Signal()
user_subscribed = Signal()
user_unsubscribed = Signal()

#
# Signals listened to
#


@receiver([user_subscribed, user_unsubscribed])
def on_user_subscribed(sender, **kwargs):
    """Clear the subscriptions cache when a user is subscribed or unsubscribed.
    """
    user_email = kwargs["user_email"]
    User = get_user_model()
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        try:
            emailaddress = EmailAddress.objects.get(email=user_email)
        except EmailAddress.DoesNotExist:
            return  # No such user
        user = emailaddress.user
    cache.delete("User:%s:subscriptions" % user.id, version=2)
    get_subscriptions(user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, **kwargs):
    """Create a Profile when a User is created"""
    user = kwargs["instance"]
    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(user=user)
    # If the current user's first or last name is not None, then update them in
    # Core.
    if user.first_name or user.last_name:
        mm_user = get_mailman_user(user)
        new_display_name = "{} {}".format(user.first_name, user.last_name)
        # Remove leading or trailing space if only first_ or last_.
        new_display_name = new_display_name.strip()
        if mm_user and mm_user.display_name != new_display_name:
            mm_user.display_name = new_display_name
            mm_user.save()
            # Also, update the names in the address objects.
            for address in mm_user.addresses:
                if address.display_name != new_display_name:
                    address.display_name = new_display_name
                    address.save()

# Allauth


@receiver(user_logged_in)
def on_user_logged_in(sender, **kwargs):
    """Sync a user's address with Core when they logs in."""
    user = kwargs["user"]
    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(user=user)
    sync_email_addresses(user)


@receiver(user_signed_up)
def on_user_signed_up(sender, **kwargs):
    # Sent when a user signs up for an account.
    user = kwargs["user"]
    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(user=user)
    # We want to add the user to Mailman with all its verified email addresses.
    for address in EmailAddress.objects.filter(user=user):
        if address.verified:
            logger.debug("Adding email address %s to user %s",
                         address.email, user.username)
            add_address_to_mailman_user(user, address.email)


@receiver(email_removed)
def on_email_removed(sender, **kwargs):
    # Sent when an email address has been removed.
    # Remove it from Mailman.
    user = kwargs["user"]
    email_address = kwargs["email_address"]
    mm_user = get_mailman_user(user)
    if mm_user is None:
        return  # Could not get the user from Mailman.
    try:
        mm_user.addresses.remove(email_address.email)
    except ValueError:
        pass  # not in Mailman's addresses


@receiver(email_confirmed)
def on_email_confirmed(sender, **kwargs):
    # Sent after the email address in the db was updated and set to confirmed.
    # Associate it with the user and set it to verified in Mailman.
    email_address = kwargs["email_address"]
    logger.debug("Confirmed email %s of user %s",
                 email_address.email, email_address.user.username)
    add_address_to_mailman_user(email_address.user, email_address.email)


@receiver(email_changed)
def on_email_changed(sender, **kwargs):
    # Sent when a primary email address has been changed.
    user = kwargs.get('user')
    to_email_address = kwargs.get('to_email_address')
    if to_email_address is None:
        return
    update_preferred_address(user, to_email_address)


@receiver(social_account_added)
def on_social_account_added(sender, **kwargs):
    # Sent after a user connects a social account to a their local account.
    # Add to mailman emails that were marked as verified by the social account
    # provider.
    sociallogin = kwargs["sociallogin"]
    logger.debug("Social account %s added for user %s",
                 sociallogin.account, sociallogin.user.username)
    for address in sociallogin.email_addresses:
        if EmailAddress.objects.filter(email=address.email).exists():
            # TODO: should we do something if it belongs so another user?
            continue
        logger.debug("Adding email address %s to user %s",
                     address.email, sociallogin.user.username)
        address.user = sociallogin.user
        address.primary = False  # There already is a primary address.
        address.save()
        if address.verified:
            add_address_to_mailman_user(sociallogin.user, address.email)
