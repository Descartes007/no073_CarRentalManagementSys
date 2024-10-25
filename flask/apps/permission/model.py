#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# Author: anonymous
# Create_Date: 2024/3/1 20:31
# Description: xxx
import datetime

from exts import db


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    permission_ids = db.Column(db.String(256), nullable=False)

    def __init__(self, p_id, username, permission_ids):
        self.id = p_id
        self.username = username
        self.permission_ids = permission_ids

    def __str__(self):
        return self.username

    def keys(self):
        return ('username', 'permission_ids')

    def __getitem__(self, item):
        return getattr(self, item)
