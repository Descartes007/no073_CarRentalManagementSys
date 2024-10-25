#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# Author: anonymous
# Create_Date: 2024/3/1 20:29
# Description: xxx
import json
from flask import Blueprint, request, jsonify
from sqlalchemy import or_, func
from apps.permission.model import Permission
from apps.car.model import *
from exts.auth import require_access_token
from exts.common import insert_audit_log
from exts.logHandler import base_logger as logger
from exts.logHandler import audit_logger

permission_bp = Blueprint('permission', __name__)
model_name='权限管理'
@permission_bp.route('/permission/add', methods=['POST'])
@require_access_token
def permission_add(current_user):
    # 查询条目是否存在
    permission_result = Permission.query.filter_by(username=request.get_json()["name"]).first()
    if permission_result is None:
        max_id_query = db.session.query(func.max(Permission.id)).scalar()
        if max_id_query is None:
            max_id = 0
        else:
            max_id = max_id_query
        try:
            col = Permission(p_id=max_id + 1, username=request.get_json()["name"],permission_ids=','.join(i for i in request.get_json()["permission_id"]))
            db.session.add(col)  # 添加一条
            # 提交事务
            db.session.commit()
            response = {"code": 0, "message": "设置成功!", "status": True}
            # audit_logger.debug("[{0}] [{1}] [添加信息: {2}]".format(request.remote_addr, model_name, request.get_json()["name"]))
            insert_audit_log(request.remote_addr, current_user, model_name, '添加信息: ' + request.get_json()["name"])
        except Exception as e:
            logger.error("commit permission info fail")
            logger.exception(e)
            response = {"code": -1, "message": "设置失败!", "status": False}
    else:
        logger.error("add permission info fail, info is exist")
        response = {"code": -1, "message": "条目已存在!", "status": False}
    logger.debug("接口请求返回:" + json.dumps(response, ensure_ascii=False))
    return jsonify(response)

@permission_bp.route('/permission/query', methods=['POST'])
@require_access_token
def permission_query(current_user):
    permission_list = []
    pageTotal = len(Permission.query.all())
    if len(request.get_json())==0:
        query_result = Permission.query.all()
    else:
        # 查询指定用户名的权限
        query_result = Permission.query.filter_by(username=request.get_json()['username']).first()
    for i in query_result:
        permission_dict = dict(i)
        permission_dict.update({"permission_ids":[i for i in permission_dict["permission_ids"].split(",")]})
        permission_list.append(permission_dict)
    response = {"status": True, "message": "查询成功", "infos": permission_list, "pageTotal": pageTotal}
    logger.debug("接口请求返回:" + json.dumps(response,ensure_ascii=False))
    return jsonify(response)