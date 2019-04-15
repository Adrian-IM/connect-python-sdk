# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from typing import Any, Dict

from connect.logger import function_log
from connect.models import ActivationTileResponse
from connect.models.base import BaseModel
from .base import BaseResource
from .template import TemplateResource


class AutomationResource(BaseResource):
    limit = 1000

    def get_filters(self, status='pending', **kwargs):
        # type: (str, Dict[str, str]) -> Dict[str, Any]
        return super(AutomationResource, self).get_filters(status=status, **kwargs)

    def process(self):
        # type: () -> None
        for request in self.get_list():
            self.dispatch(request)

    def dispatch(self, request):
        # type: (BaseModel) -> str
        raise NotImplementedError('Please implement `{}.dispatch` method'
                                  .format(self.__class__.__name__))

    def process_request(self, request):
        raise NotImplementedError('Please implement `{}.process_request` method'
                                  .format(self.__class__.__name__))

    @function_log
    def approve(self, pk, data):
        # type: (str, dict) -> str
        return self.api.post(path=pk + '/approve/', json=data)

    @function_log
    def inquire(self, pk):
        # type: (str) -> str
        return self.api.post(path=pk + '/inquire/', json={})

    @function_log
    def fail(self, pk, reason):
        # type: (str, str) -> str
        return self.api.post(path=pk + '/fail/', json={'reason': reason})

    @function_log
    def render_template(self, pk, template_id):
        # type: (str, str) -> ActivationTileResponse
        return TemplateResource(self.config).render(template_id, pk)
