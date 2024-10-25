
'''
**************************************************************
** @Create：2024/2/26 10:50
** @Author：anonymous
** @Description：
**************************************************************
'''
import hashlib
import json
import os

from flask import Blueprint, request, jsonify, session, url_for

from sqlalchemy import or_, func
from werkzeug.utils import secure_filename

import settings
from apps.brand.model import Brand
from apps.car.model import *
from exts.auth import require_access_token
from exts.common import insert_audit_log
from exts.logHandler import base_logger as logger
from exts.logHandler import audit_logger

brand_bp = Blueprint('brand', __name__)
model_name='汽车品牌管理'
@brand_bp.route('/brand/add', methods=['POST'])
@require_access_token
def brand_add(current_user):
    # 查询条目是否存在
    obj = Brand.query.filter_by(name=request.get_json()["name"]).first()
    if obj is None:
        max_id_query = db.session.query(func.max(Brand.id)).scalar()
        if max_id_query is None:
            max_id = 0
        else:
            max_id = max_id_query
        try:
            col = Brand(brand_id=max_id + 1, name=request.get_json()["name"],photo=request.get_json()["photo"])
            db.session.add(col)  # 添加一条
            # 提交事务
            db.session.commit()
            response = {"code": 0, "message": "创建成功!", "status": True}
            insert_audit_log(request.remote_addr, current_user, model_name, '添加汽车品牌: ' + request.get_json()["name"])
        except Exception as e:
            logger.error("commit brand info fail")
            logger.exception(e)
            response = {"code": -1, "message": "创建失败!", "status": False}
    else:
        logger.error("add brand info fail, info is exist")
        response = {"code": -1, "message": "条目已存在!", "status": False}
    logger.debug("接口请求返回:" + json.dumps(response,ensure_ascii=False))
    return jsonify(response)



@brand_bp.route('/brand/update', methods=['POST'])
@require_access_token
def brand_update(current_user):
    try:
        Brand.query.filter_by(id=request.get_json()["id"]).update({'name': request.get_json()["name"]})
        # 提交更新到数据库（事务提交）
        db.session.commit()
        response = {"code": 0, "message": "保存成功!", "status": True}
        insert_audit_log(request.remote_addr, current_user, model_name, '更新汽车品牌: ' + request.get_json()["name"])
    except Exception as e:
        logger.error("update brand info fail")
        logger.exception(e)
        response = {"code": -1, "message": "保存失败!", "status": False}
    logger.debug("接口请求返回:" + json.dumps(response))
    return jsonify(response)

@brand_bp.route('/brand/query', methods=['POST'])
@require_access_token
def brand_query(current_user):
    query_list = []
    pageTotal = len(Brand.query.all())
    if len(request.get_json())==0:
        query_result = Brand.query.all()
    else:
        query_string = request.get_json()['query_string']
        # 指定分页信息查询数据
        if query_string == '':
            page = int(request.get_json()['page'])
            size = int(request.get_json()['size'])
            offset = (page - 1) * size
            query_result=Brand.query.offset(offset).limit(size).all()
        # 指定关键字查询
        else:
            query_result = Brand.query.filter((Brand.name.contains(query_string))).all()
            pageTotal=len(query_result)
    for i in query_result:
        brand = i.to_dict()
        if i.photo:
            photo_addr = 'http://' + settings.Config.SERVER_IP + ":" + str(settings.Config.SERVER_PORT) + i.photo
        else:
            photo_addr = ''
        brand['photo'] = photo_addr
        query_list.append(brand)
    response = {"status": True, "message": "查询成功", "infos": query_list, "pageTotal": pageTotal}
    logger.debug("接口请求返回:" + json.dumps(response,ensure_ascii=False))
    return jsonify(response)

@brand_bp.route('/brand/count', methods=['POST'])
@require_access_token
def brand_count(current_user):
    count = len(Brand.query.all())
    response = {"status": True, "message": "统计成功", "count": count}
    logger.debug("接口请求返回:" + json.dumps(response,ensure_ascii=False))
    return jsonify(response)


@brand_bp.route('/brand/delete', methods=['POST'])
@require_access_token
def brand_delete(current_user):
    failed_item_ids = []
    if not isinstance(request.get_json()["id"],list):
        delete_ids=[request.get_json()["id"]]
    else:
        delete_ids = request.get_json()["id"]
    for del_id in delete_ids:
        obj = Brand.query.get(del_id)
        # 判断该条目是否存在
        if obj is None:
            logger.error("delete {0} from table brand fail".format(request.get_json()))
            failed_item_ids.append(del_id)
        else:
            try:
                db.session.delete(obj)  # 将对象放在缓存中准备删除
                db.session.commit()  # 提交事务，删除
                os.popen("del "+settings.Config.UPLOAD_FOLDER.replace('/','\\') +"\\brand\\"+obj.photo.split('/')[-1])
                logger.success("delete {0} from table brand success".format(request.get_json()))
                insert_audit_log(request.remote_addr, current_user, model_name,'删除汽车品牌: ' + str(request.get_json()["id"]))
            except Exception as e:
                logger.exception(e)
                db.session.rollback()
                failed_item_ids.append(del_id)
                logger.error("delete {0}  from table brand fail".format(request.get_json()))
    if len(failed_item_ids) == 0:
        response = {"status": True, "code": 0, "message": '删除成功'}
    elif len(failed_item_ids) == len(delete_ids):
        response = {"status": False, "code": -2, "message": '删除失败'}
    else:
        response = {"status": True, "code": -1, "message": '部分条目删除失败'}
    logger.debug("接口请求返回:" + json.dumps(response,ensure_ascii=False))
    return jsonify(response)

@brand_bp.route('/upload', methods=['POST'])
@require_access_token
def file_upload(current_user):
    file = request.files['file']
    if file:
        # 上传的文件名
        filename = secure_filename(file.filename)
        # 将文件保存到服务器指定目录
        file_path = settings.Config.UPLOAD_FOLDER +"\\brand\\" +filename
        try:
            file.save(file_path)
            # 计算图片md5值作为图片ID
            md5_obj = hashlib.md5()
            with open(file_path, 'rb') as file_obj:
                md5_obj.update(file_obj.read())
            img_id = md5_obj.hexdigest()
            new_file_name = img_id + "." + file.filename.split('.')[-1]
            # 对服务器存储的资源文件进行重命名并返回该图片的路径
            if not os.path.exists(settings.Config.UPLOAD_FOLDER +"\\brand\\" + new_file_name):
                os.rename(file_path, settings.Config.UPLOAD_FOLDER +"\\brand\\" + new_file_name)
                response = {'code': 0, 'message': '上传成功', 'path': '/images/brand/'+new_file_name,
                            'status': True}
                insert_audit_log(request.remote_addr, current_user, model_name, '上传了文件: ' + filename)
            else:
                response = {'code': -1, 'message': '文件已存在', 'status': False}
        except Exception as e:
            logger.exception(e)
            response = {'code': -1, 'message': '上传失败', 'status': False}
        logger.debug("接口请求返回:" + json.dumps(response, ensure_ascii=False))
        return jsonify(response)