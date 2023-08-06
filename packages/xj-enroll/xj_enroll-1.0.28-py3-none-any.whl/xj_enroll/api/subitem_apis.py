from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from xj_enroll.service.subitem_service import SubitemService
from xj_user.utils.user_wrapper import user_authentication_wrapper
from ..utils.custom_response import util_response
from ..utils.model_handle import parse_data


class SubitemApis(APIView):

    @require_http_methods(['GET'])
    @user_authentication_wrapper
    def list(self, *args, **kwargs, ):
        request_params = parse_data(self)
        data, err = SubitemService.list(params=request_params)

        if err:
            return util_response(err=1000, msg=data)
        return util_response(data=data)

    @require_http_methods(['POST'])
    def add(self, *args, **kwargs, ):
        params = parse_data(self)
        data, err = SubitemService.add(params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['PUT'])
    def edit(self, *args, **kwargs, ):
        params = parse_data(self)
        subitem_id = params.pop("id", None) or kwargs.pop("pk", None)
        data, err = SubitemService.edit(params, subitem_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
