# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import functools
from typing import Any, List, Dict, Union

import requests
from requests import compat

from connect.config import Config
from connect.logger import function_log, logger
from connect.models import BaseSchema, ServerErrorSchema
from connect.models.exception import ServerErrorException


class ApiClient(object):
    def __init__(self, config, base_path):
        # type: (Config, str) -> None

        # Set base URL
        self._base_path = base_path

        # Set passed config or globally configured instance
        self._config = config or Config.get_instance()
        if not isinstance(self._config, Config):
            raise ValueError('A valid Config object must be passed or globally configured.')

    @property
    def base_path(self):
        # type: () -> str
        return self._base_path

    @property
    def config(self):
        # type: () -> Config
        return self._config

    @property
    def headers(self):
        # type: () -> Dict[str, str]
        return {
            'Authorization': (self.config.api_key
                              if self.config.api_key.startswith('ApiKey ')
                              else 'ApiKey ' + self.config.api_key),
            'Content-Type': 'application/json',
        }

    def get_url(self, path=''):
        # type: (str) -> str
        return self.urljoin(self.config.api_url, self.base_path, path)

    @staticmethod
    def urljoin(*args):
        return functools.reduce(
            lambda a, b: compat.urljoin(a + ('' if a.endswith('/') else '/'), b),
            args)

    @function_log
    def get(self, path='', **kwargs):
        kwargs = self._fix_request_kwargs(path, kwargs)
        response = requests.get(**kwargs)
        return self._check_response(response)

    @function_log
    def post(self, path='', **kwargs):
        kwargs = self._fix_request_kwargs(path, kwargs)
        response = requests.post(**kwargs)
        return self._check_response(response)

    @function_log
    def put(self, path='', **kwargs):
        kwargs = self._fix_request_kwargs(path, kwargs)
        response = requests.put(**kwargs)
        return self._check_response(response)

    def _fix_request_kwargs(self, path, prev_kwargs, **kwargs):
        # type: (str, Dict[str, Any], Dict[str, Any]) -> Dict[str, Any]
        """ Set correct kwargs for requests """
        fixed_kwargs = prev_kwargs.copy()
        fixed_kwargs.update(kwargs)
        if 'url' not in fixed_kwargs:
            fixed_kwargs['url'] = self.get_url(path)
        if 'headers' not in fixed_kwargs:
            fixed_kwargs['headers'] = self.headers
        return fixed_kwargs

    @staticmethod
    def _check_response(response):
        # type: (requests.Response) -> str
        if not hasattr(response, 'content'):
            raise AttributeError(
                'Response does not have attribute content. Check your request params. '
                'Response status - {}'.format(response.status_code),
            )

        if not hasattr(response, 'ok') or not response.ok:
            data, error = ServerErrorSchema().loads(response.content)
            if data:
                raise ServerErrorException(data)

        return response.content


class BaseResource(object):
    resource = None  # type: str
    limit = 100  # type: int
    schema = BaseSchema()  # type: BaseSchema

    def __init__(self, config=None):
        # Set api
        if not self.__class__.resource:
            raise AttributeError('Resource name not specified in class {}. '
                                 'Add an attribute `resource` with the name of the resource'
                                 .format(self.__class__.__name__))
        self._api = ApiClient(config, self.__class__.resource)

    @property
    def api(self):
        # type: () -> ApiClient
        return self._api

    @property
    def config(self):
        # type: () -> Config
        return self.api.config

    def get(self, pk):
        # type: (str) -> Any
        response = self.api.get(path=pk)
        objects = self._load_schema(response)
        if isinstance(objects, list) and len(objects) > 0:
            return objects[0]

    def get_filters(self):
        # type: () -> Dict[str, Any]
        filters = {}
        if self.limit:
            filters['limit'] = self.limit
        return filters

    def get_list(self, filters=None):
        # type: (Dict[str, Any]) -> List[Any]
        filters = filters or self.get_filters()
        logger.info('Get list request with filters - {}'.format(filters))
        response = self.api.get(params=filters)
        return self._load_schema(response)

    def _load_schema(self, response, many=None, schema=None):
        # type: (str, bool, BaseSchema) -> Union[List[Any], Any]
        schema = schema or self.schema
        objects, error = schema.loads(response, many)
        if error:
            raise TypeError(
                'Invalid structure for initialization of `{}`. \n'
                'Error: {}. \nServer Response: {}'.format(type(self).__name__, error, response),
            )
        return objects
