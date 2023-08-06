# encoding: utf-8
"""
@project: djangoModel->subitem_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 报名分项记录
@created_time: 2022/10/15 12:38
"""

from django.core.paginator import Paginator
from django.db.models import F

from ..models import EnrollSubitem
from ..service.subitem_extend_service import input_convert, output_convert
from ..utils.model_handle import format_params_handle


class SubitemService:
    @staticmethod
    def add(params):
        enroll_id = params.get("enroll_id")
        if not enroll_id:
            return None, "请填写报名ID"

        params = input_convert(
            params_dict=params,
            enroll_id=enroll_id
        )
        try:
            instance = EnrollSubitem.objects.create(**params)
            return instance.to_json(), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def list(params, is_pagination=True):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        # 字段过滤
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "enroll_id", "name", "price", "count", "unit", "description", "remark"],
        )
        try:
            fetch_obj = EnrollSubitem.objects.annotate(category_id=F("enroll__category_id")).filter(**params).values()
            paginator = Paginator(fetch_obj, size)
            page_obj = paginator.page(page)
            result_list = list(page_obj.object_list)
            result_list = output_convert(result_list)
            if not is_pagination:
                return result_list, None
            data = {'total': paginator.count, "size": size, 'page': page, 'list': result_list}
            return data, None
        except Exception as e:
            print(e)
            return [], str(e)

    @staticmethod
    def edit(params, subitem_id=None):
        # 参数验证
        subitem_id = subitem_id or params.pop("id", None) or 0
        subitem_obj = EnrollSubitem.objects.filter(id=subitem_id)
        if not subitem_obj:
            return None, "找不到ID为" + str(subitem_id) + "的数据"
        # 开始修改
        try:
            enroll_id = params.get("enroll_id") or subitem_obj.first().to_json().get("enroll_id")
            # 参数解析
            params = input_convert(
                params_dict=params,
                enroll_id=enroll_id
            )
            subitem_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    # 批量修改
    @staticmethod
    def batch_edit(params, enroll_id=None):
        enroll_id = enroll_id or params.pop("enroll_id", None)
        if not enroll_id:
            return None, "请填写报名ID"

        params = input_convert(
            params_dict=params,
            enroll_id=enroll_id
        )

        subitem_enroll_obj = EnrollSubitem.objects.filter(enroll_id=enroll_id)
        if not subitem_enroll_obj:
            return None, None
        try:
            subitem_enroll_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def delete(subitem_rule_id):
        subitem_enroll_obj = EnrollSubitem.objects.filter(id=subitem_rule_id)
        if not subitem_enroll_obj:
            return None, None
        try:
            subitem_enroll_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None
