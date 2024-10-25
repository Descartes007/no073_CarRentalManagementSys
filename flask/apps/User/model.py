#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Time    : 2023年03月18日18:57分
@Author  : Anonymous
@Description: 普通用户模型
'''
from datetime import datetime
from exts import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(11), unique=True)
    role_id = db.Column(db.Integer)
    register_time = db.Column(db.DateTime, default=datetime.now())
    last_login_time = db.Column(db.DateTime, default=datetime.now())
    ip = db.Column(db.String(15))
    description = db.Column(db.String(256))
    car_collect_list = db.Column(db.String(1024))

    def __init__(self, u_id, username, password, email, phone, role_id=2):
        self.id = u_id
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.role_id = int(role_id)


    def __str__(self):
        return self.username

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role_id': self.role_id,
            'phone': self.phone,
            'register_time': self.register_time,
            'last_login_time': self.last_login_time,
            'ip': self.ip,
            'description': self.description
        }
