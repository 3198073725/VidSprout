#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')
django.setup()

from files.models import Media
from users.models import User

# 检查媒体
m = Media.objects.filter(friendly_token='SrZKGJuVS').first()
if m:
    print("Media found:")
    print(f"   - Title: {m.title}")
    print(f"   - Owner: {m.user}")
    print(f"   - State: {m.state}")
    print(f"   - Featured: {m.featured}")
    print(f"   - Enable comments: {m.enable_comments}")
else:
    print("Media not found")

# 检查当前用户
user = User.objects.filter(email='13030427438@163.com').first()
if user:
    print(f"\nUser found:")
    print(f"   - Username: {user.username}")
    print(f"   - Is editor: {user.is_editor}")
    print(f"   - Is manager: {user.is_manager}")
    
    if m:
        print(f"\nPermission check:")
        print(f"   - Is owner: {user == m.user}")
        print(f"   - Can edit: {user.has_contributor_access_to_media(m)}")

