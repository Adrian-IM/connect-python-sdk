# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import os
from collections import namedtuple

from mock import MagicMock, patch

from connect import TierConfigAutomation
from connect.models import Param
from connect.models.base import BaseModel
from connect.models.company import Company
from connect.models.connection import Connection
from connect.models.hub import Hub
from connect.models.product import Product
from connect.models.tier_config import TierConfigRequest, TierConfig, Events, Template, \
    Activation, EventInfo, Account

Response = namedtuple('Response', ('ok', 'content'))


def _get_response_ok():
    with open(os.path.join(os.path.dirname(__file__), 'response_tier_config_request.json'))\
            as file_handle:
        content = file_handle.read()
    return Response(ok=True, content=content)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_create_resource():
    requests = TierConfigAutomation().list
    assert isinstance(requests, list)
    assert len(requests) == 1

    request = requests[0]
    assert isinstance(request, TierConfigRequest)
    assert request.id == 'TCR-000-000-000'
    assert request.type == 'setup'
    assert request.status == 'pending'

    configuration = request.configuration
    assert isinstance(configuration, TierConfig)
    assert configuration.id == 'TC-000-000-000'
    assert configuration.name == 'Configuration of Reseller'
    assert configuration.tier_level == 1

    account = configuration.account
    assert isinstance(account, Account)
    assert account.id == 'TA-1-000-000-000'

    product = configuration.product
    assert isinstance(product, Product)
    assert product.id == 'PRD-000-000-000'
    assert product.name == 'Product'

    connection = configuration.connection
    assert isinstance(connection, Connection)
    assert connection.id == 'CT-9861-7949-8492'
    assert connection.type == 'production'

    hub = connection.hub
    assert isinstance(hub, Hub)
    assert hub.id == 'HB-12345-12345'
    assert hub.name == 'Provider Production Hub'

    provider = connection.provider
    assert isinstance(provider, Company)
    assert provider.id == 'PA-9861-7949'
    assert provider.name == 'Ingram Micro Prod DA'

    vendor = connection.vendor
    assert isinstance(vendor, Company)
    assert vendor.id == 'VA-9861-7949'
    assert vendor.name == 'Large Largo and Co'

    events = configuration.events
    assert isinstance(events, Events)
    assert isinstance(events.created, EventInfo)
    assert events.created.at == '2018-11-21T11:10:29+00:00'
    assert not events.created.by
    assert not events.inquired
    assert not events.pended
    assert not events.validated
    assert isinstance(events.updated, EventInfo)
    assert events.updated.at == '2018-11-21T11:10:29+00:00'
    assert isinstance(events.updated.by, Company)
    assert events.updated.by.id == 'PA-000-000'
    assert events.updated.by.name == 'Username'

    params = configuration.params
    assert isinstance(params, list)
    assert len(request.params) == 1
    assert isinstance(request.params[0], Param)
    assert request.params[0].id == 'param_a'
    assert request.params[0].value == 'param_a_value'

    open_request = configuration.open_request
    assert isinstance(open_request, BaseModel)
    assert open_request.id == 'TCR-000-000-000'

    template = configuration.template
    assert isinstance(template, Template)
    assert template.id == 'TP-000-000-000'
    assert template.representation == 'Render text is here......'

    events = request.events
    assert isinstance(events, Events)
    assert isinstance(events.created, EventInfo)
    assert events.created.at == '2018-11-21T11:10:29+00:00'
    assert not events.created.by
    assert isinstance(events.inquired, EventInfo)
    assert events.inquired.at == '2018-11-21T11:10:29+00:00'
    assert isinstance(events.inquired.by, Company)
    assert events.inquired.by.id == 'PA-000-000'
    assert events.inquired.by.name == 'Username'
    assert isinstance(events.pended, EventInfo)
    assert events.pended.at == '2018-11-21T11:10:29+00:00'
    assert isinstance(events.pended.by, Company)
    assert events.pended.by.id == 'PA-000-001'
    assert events.pended.by.name == 'Username1'
    assert not events.validated
    assert not events.updated

    params = request.params
    assert isinstance(params, list)
    assert len(request.params) == 1
    assert isinstance(request.params[0], Param)
    assert request.params[0].id == 'param_a'
    assert request.params[0].value == 'param_a_value'

    assignee = request.assignee
    assert isinstance(assignee, Company)
    assert assignee.id == 'PA-000-000'
    assert assignee.name == 'Username'

    template = request.template
    assert isinstance(template, Template)
    assert template.id == 'TP-000-000-000'
    assert template.representation == 'Render text is here......'

    activation = request.activation
    assert isinstance(activation, Activation)
    assert activation.link == 'http://example.com'


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_process():
    automation = TierConfigAutomation()
    automation.process()


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_get_tier_config():
    config = TierConfigAutomation().get_tier_config('', '')
    assert isinstance(config, TierConfig)


@patch('requests.get', MagicMock(return_value=Response(ok=True, content='[]')))
def test_get_tier_config_empty():
    config = TierConfigAutomation().get_tier_config('', '')
    assert not config


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_get_tier_config_param():
    tier_config = TierConfigAutomation().get_tier_config('', '')
    param = tier_config.get_param_by_id('param_a')
    assert isinstance(param, Param)
    assert param.id == 'param_a'
    assert param.value == 'param_a_value'
