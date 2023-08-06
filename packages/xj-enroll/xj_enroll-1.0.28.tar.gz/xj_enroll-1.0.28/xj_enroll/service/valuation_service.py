# encoding: utf-8
"""
@project: djangoModel->valuation_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 计价生成服务
@created_time: 2022/10/13 9:40
"""

from ..models import Enroll, EnrollRuleValuate
# 接口服务类
from ..service.subitem_service import SubitemService
from ..utils.j_valuation import JExpression


class ValuationService:
    expression = None  # 表达式

    @staticmethod
    def valuate(expression_string=None, input_dict=None):
        # 测试代码
        if input_dict is None:
            input_dict = {}

        expression_string, parsed_variable_map = JExpression.parse_variables(
            expression_string,
            input_dict
        )
        calculator = JExpression()
        data, err = calculator.process(expression_string)
        return data, err

    @staticmethod
    def valuate_result(enroll_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, "不存在该报名信息"
        # 变量字典
        variables_dict = enroll_obj.first().to_json()

        # 获取计价ID
        enroll_rule_group_id = variables_dict.get("enroll_rule_group_id")
        if not enroll_rule_group_id:
            return None, "该报名没有绑定计价ID"

        # 获取计价规则
        valuate_obj = EnrollRuleValuate.objects.filter(enroll_rule_group_id=enroll_rule_group_id)
        if not valuate_obj:
            return None, "没有配置计价公式"

        # 子项变量
        subitem_list, err = SubitemService.list({"enroll_id": enroll_id}, False)
        subitem_dict = {}
        for i in subitem_list:
            for k, v in i.items():
                key = "enroll_subitem__" + k
                value = str(v) if v else "0"
                subitem_dict[key] = value if (subitem_dict.get(key, None) is None) else (subitem_dict[key] + "," + value)
        variables_dict.update(subitem_dict)

        # 计算公式解析
        result = {}
        valuate_list = valuate_obj.values("name", "type", "field", "expression_string")
        for item in valuate_list:
            expression_string, parsed_variable_map = JExpression.parse_variables(
                item["expression_string"],
                variables_dict
            )
            calculator = JExpression()
            data, err = calculator.process(expression_string)
            result[item["field"]] = data
        return result, None
