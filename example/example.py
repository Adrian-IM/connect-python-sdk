# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from connect import FulfillmentAutomation
from connect.config import Config
from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip
from connect.models.fulfillment import Fulfillment

# Set logger level / default level ERROR
logger.setLevel("DEBUG")

# If we remove this line, it is done implicitly
Config(filename='config.json')


class ExampleRequestProcessor(FulfillmentAutomation):
    def process_request(self, request):
        # type: (Fulfillment) -> object

        logger.info('Processing request {}'.format(request.id))

        # Custom logic
        if request.type == 'purchase':
            for item in request.asset.items:
                if item.quantity > 100000:
                    raise FulfillmentFail(
                        message='Is Not possible to purchase product')

            for param in request.asset.params:
                if param.name == 'email' and not param.value:
                    param.value_error = 'Email address has not been provided, please provide one'
                    raise FulfillmentInquire(params=[param])

            # Approve by ActivationTile
            return ActivationTileResponse('\n  # Welcome to Fallball!\n\nYes, you decided '
                                          'to have an account in our amazing service!')
            # Or
            # return TemplateResource().render(pk='TEMPLATE_ID', request_id=request.id)

            # Approve by Template
            # noinspection PyUnreachableCode
            return ActivationTemplateResponse('TL-497-535-242')
            # Or
            # return TemplateResource().get(pk='TEMPLATE_ID')

        elif request.type == 'change':
            # Fail
            raise FulfillmentFail()
        else:
            # Skip request
            raise Skip()


if __name__ == '__main__':
    request_processor = ExampleRequestProcessor()
    request_processor.process()
