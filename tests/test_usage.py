# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import os
import time
from collections import namedtuple
from datetime import date, timedelta

import pytest
from mock import patch, MagicMock

from connect.models import usage
from connect.models.exception import FileRetrievalError
from connect.models.marketplace import Contract
from connect.models.product import Product
from connect.resource import UsageAutomation

Response = namedtuple('Response', ('ok', 'content', 'text', 'status_code'))


def _get_response_ok():
    with open(os.path.join(os.path.dirname(__file__), 'response_usage.json')) as file_handle:
        content = file_handle.read()
    return Response(ok=True, content=content, text='', status_code=200)


def _get_response_ok2():
    with open(os.path.join(os.path.dirname(__file__), 'response_usage2.json')) as file_handle:
        content = file_handle.read()
    return Response(ok=True, content=content, text='', status_code=201)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_create_resource():
    requests = UsageAutomation().list
    assert isinstance(requests, list)
    assert len(requests) == 8


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
@patch('requests.post', MagicMock(return_value=_get_response_ok2()))
def test_process():
    resource = UsageAutomationTester()
    resource.process()


@patch('requests.get', MagicMock(
    return_value=Response(ok=True, content='{"template_link": "..."}', text='test', status_code=200)))
def test_get_usage_template_ok():
    assert UsageAutomation().get_usage_template(Product(id='PRD-638-321-603')) == 'test'


@patch('requests.get', MagicMock(return_value=Response(ok=True, content='{}', text='', status_code=200)))
def test_get_usage_template_no_link():
    with pytest.raises(FileRetrievalError):
        UsageAutomation().get_usage_template(Product(id='PRD-638-321-603'))


@patch('requests.get', MagicMock(return_value=Response(
    ok=True, content='{"template_link": "..."}', text=None, status_code=200)))
def test_get_usage_template_no_file():
    with pytest.raises(FileRetrievalError):
        UsageAutomation().get_usage_template(Product(id='PRD-638-321-603'))


class UsageAutomationTester(UsageAutomation):
    def process_request(self, request):
        # type: (usage.File) -> None
        if request.contract.id == 'CRD-99082-45842-69181':
            usage_file = usage.File(
                name='sdk test',
                product=Product(id=request.product.id),
                contract=Contract(id=request.contract.id)
            )
            usages = [usage.FileUsageRecord(
                item_search_criteria='item.mpn',
                item_search_value='SKUA',
                quantity=1,
                start_time_utc=(date.today() - timedelta(1)).strftime('%Y-%m-%d'),
                end_time_utc=time.strftime('%Y-%m-%d %H:%M:%S'),
                asset_search_criteria='parameter.param_b',
                asset_search_value='tenant2'
            )]
            self.submit_usage(usage_file, usages)
        elif request.contract.id == 'CRD-99082-45842-69182':
            pass
        elif request.contract.id == 'CRD-99082-45842-69183':
            pass
