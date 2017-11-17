# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from user.models import User
from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
