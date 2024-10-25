#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/2/27 15:32
** @Author：anonymous
** @Description： 全局路由，不属于任何app组件
**************************************************************
'''
import json
import re
import settings
from flask import Blueprint, request, jsonify, app
from exts.auth import require_access_token

global_bp = Blueprint('global', __name__)


