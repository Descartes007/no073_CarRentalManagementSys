#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# Author: anonymous
# Create_Date: 2024/3/10 10:41
# Description: 汽车品牌模型
from exts import db


class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    photo = db.Column(db.String(128))
    # 一个品牌可以有很多车辆,backref='backref_brand'用于通过汽车实例.backref_brand就可以找到品牌实例,backref参数来创建反向引用
    cars = db.relationship('Car', backref='backref_brand', lazy='dynamic')

    def __init__(self, brand_id, name, photo):
        self.id = brand_id
        self.name = name
        self.photo = photo

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'photo': self.photo}
