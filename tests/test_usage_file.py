# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import os

import pytest
from mock import patch, MagicMock

from connect.models import Company, SkipRequest, AcceptUsageFile, CloseUsageFile, DeleteUsageFile, \
    RejectUsageFile, SubmitUsageFile, Contract, Marketplace, Product, Records, File
from connect.resource import UsageFileAutomation
from .common import Response, load_str

current_action = ''


# noinspection PyUnusedLocal
def _get_response_ok(*args, **kwargs):
    content = load_str(os.path.join(os.path.dirname(__file__), 'data', 'response_usage_file.json'))
    if current_action:
        content = content.replace('UF-2018-11-9878764342',
                                  'UF-2018-11-9878764342-' + current_action)
    return Response(ok=True, content=content, status_code=200)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_create_resource():
    requests = UsageFileAutomationTester().list()
    assert isinstance(requests, list)
    assert len(requests) == 1

    request = requests[0]
    assert isinstance(request, File)
    assert request.id == 'UF-2018-11-9878764342'
    assert request.name == 'Usage for Feb 2019'
    assert request.description == 'Usage for the product belonging to month Feb 2019'
    assert request.note == 'My personal note'
    assert request.status == 'READY'
    assert request.created_by == 'rahul.mondal@ingrammicro.com'
    assert request.created_at == '2018-11-21T11:10:29+00:00'

    product = request.product
    assert isinstance(product, Product)
    assert product.id == 'CN-631-322-000'
    assert product.name == 'Google Apps'
    assert product.icon == '/media/VA-587-127/CN-783-317-575/media/CN-783-317-575-logo.png'

    contract = request.contract
    assert isinstance(contract, Contract)
    assert contract.id == 'CRD-00000-00000-00000'
    assert contract.name == 'ACME Distribution Contract'

    marketplace = request.marketplace
    assert isinstance(marketplace, Marketplace)
    assert marketplace.id == 'MP-198987'
    assert marketplace.name == 'France'
    assert marketplace.icon == '/media/PA-123-123/marketplaces/MP-12345/image.png'

    vendor = request.vendor
    assert isinstance(vendor, Company)
    assert vendor.id == 'VA-587-127'
    assert vendor.name == 'Symantec'

    provider = request.provider
    assert isinstance(provider, Company)
    assert provider.id == 'PA-587-127'
    assert provider.name == 'ABC Corp'

    assert request.upload_file_uri == '<File Location for uploaded file>'
    assert request.processed_file_uri == '<File Location for generated file>'
    assert request.acceptance_note == 'All usage data is correct'
    assert request.rejection_note == 'Rejected due to wrong usage for item 56'
    assert request.error_detail == 'Error details in case of usage file is marked as invalid'

    records = request.records
    assert isinstance(records, Records)
    assert records.valid == 56
    assert records.invalid == 0

    assert request.uploaded_by == 'rahul.mondal@ingrammicro.com'
    assert request.uploaded_at == '2018-11-21T11:10:29+00:00'
    assert request.submitted_by == 'rahul.mondal@ingrammicro.com'
    assert request.submitted_at == '2018-11-21T11:10:29+00:00'
    assert request.accepted_by == 'admin@a1provider.com'
    assert request.accepted_at == '2018-11-21T11:10:29+00:00'
    assert request.rejected_by == 'admin@a1provider.com'
    assert request.rejected_at == '2018-11-21T11:10:29+00:00'
    assert request.closed_by == 'admin@a1provider.com'
    assert request.closed_at == '2018-11-21T11:10:29+00:00'


@patch('requests.get', MagicMock(side_effect=_get_response_ok))
@patch('requests.post', MagicMock())
def test_process():
    global current_action
    actions = ['accept', 'close', 'delete', 'reject', 'submit', 'skip']
    resource = UsageFileAutomationTester()

    # If process_request does not return an exception (as with default id), a UserWarning is raised
    with pytest.raises(UserWarning):
        resource.process()

    # Test that all other actions do not raise UserWarning
    for action in actions:
        current_action = action  # This is used by _get_response_ok to define request id
        resource.process()


class UsageFileAutomationTester(UsageFileAutomation):
    def process_request(self, request):
        # type: (File) -> None
        if request.id == 'UF-2018-11-9878764342-accept':
            raise AcceptUsageFile('Valid file moving forward')
        elif request.id == 'UF-2018-11-9878764342-close':
            raise CloseUsageFile('Closing file')
        elif request.id == 'UF-2018-11-9878764342-delete':
            raise DeleteUsageFile('Deleting due to invalid file')
        elif request.id == 'UF-2018-11-9878764342-reject':
            raise RejectUsageFile('Rejecting the file as a test')
        elif request.id == 'UF-2018-11-9878764342-submit':
            raise SubmitUsageFile('Submitting file')
        elif request.id == 'UF-2018-11-9878764342-skip':
            raise SkipRequest('Skipping')
