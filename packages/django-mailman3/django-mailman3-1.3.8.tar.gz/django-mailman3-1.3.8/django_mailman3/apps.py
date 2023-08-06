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

from django.apps import AppConfig


# For a library, adding a NullHandler is a good idea. If the Django project
# wants, they can configure the handler in LOGGING config for `django_mailman3`
# logger.
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class DjangoMailman3Config(AppConfig):
    name = 'django_mailman3'
    verbose_name = "Django Mailman 3"

    def ready(self):
        import django_mailman3.signals  # noqa: F401
