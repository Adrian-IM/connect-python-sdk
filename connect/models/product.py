# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import fields, post_load
from typing import List, Optional, Union

from .base import BaseModel, BaseSchema


class ProductConfiguration(BaseModel):
    """ Product configurations. """
    suspend_resume_supported = None  # type: bool
    """ (bool) Is suspend and resume supported for the product? """

    requires_reseller_information = None  # type: bool
    """ (bool) Does the product require reseller information? """


class ProductConfigurationSchema(BaseSchema):
    suspend_resume_supported = fields.Bool()
    requires_reseller_information = fields.Bool()

    @post_load
    def make_object(self, data):
        return ProductConfiguration(**data)


class DownloadLink(BaseModel):
    """ Download link for a product. """

    title = None  # type: str
    """ (str) Link title. """

    url = None  # type: str
    """ (str) Link URL. """


class DownloadLinkSchema(BaseSchema):
    title = fields.Str()
    url = fields.Str()

    @post_load
    def make_object(self, data):
        return DownloadLink(**data)


class Document(BaseModel):
    """ Document for a product. """

    title = None  # title: str
    """ (str) Document title. """

    url = None  # title: str
    """ (str) Document URL. """

    visible_for = None  # title: str
    """ (str) Document visibility. One of: admin, user. """


class DocumentSchema(BaseSchema):
    title = fields.Str()
    url = fields.Str()
    visible_for = fields.Str()

    @post_load
    def make_object(self, data):
        return Document(**data)


class CustomerUiSettings(BaseModel):
    """ Customer Ui Settings for a product. """

    description = None  # type: str
    """ (str) Description. """

    getting_started = None  # type: str
    """ (str) Getting started. """

    download_links = None  # type: List[DownloadLink]
    """ (List[:py:class:`.DownloadLink`]) Download links. """

    documents = None  # type: List[Document]
    """ (List[:py:class:`.Document`]) Documents. """


class CustomerUiSettingsSchema(BaseSchema):
    description = fields.Str()
    getting_started = fields.Str()
    download_links = fields.Nested(DownloadLinkSchema, many=True)
    documents = fields.Nested(DocumentSchema, many=True)

    @post_load
    def make_object(self, data):
        return CustomerUiSettings(**data)


class Product(BaseModel):
    """ Represents basic marketing information about salable items, parameters, configurations,
    latest published version and connections.

    It contains basic product information like name, description and logo, along with the latest
    published version details. So in a single point we can say a single product object always
    represent the latest published version of that product.
    """

    name = None  # type: str
    """ (str) Product name. """

    icon = None  # type: str
    """ (str) Product icon URI. """

    short_description = None  # type: str
    """ (str) Short description of product. """

    detailed_description = None  # type: str
    """ (str) Detailed description of product. """

    version = None  # type: int
    """ (int) Version of product. """

    configurations = None  # type: ProductConfiguration
    """ (:py:class:`.ProductConfiguration`) Product configuration. """

    customer_ui_settings = None  # type: CustomerUiSettings
    """ (:py:class:`.CustomerUiSettings`) Customer Ui Settings. """


class ProductSchema(BaseSchema):
    name = fields.Str()
    icon = fields.Str()
    short_description = fields.Str()
    detailed_description = fields.Str()
    version = fields.Int()
    configurations = fields.Nested(ProductConfigurationSchema)
    customer_ui_settings = fields.Nested(CustomerUiSettingsSchema)

    @post_load
    def make_object(self, data):
        return Product(**data)


class Renewal(BaseModel):
    """ Item renewal data. """

    from_ = None  # type: str
    """ (str) Date of renewal beginning. """

    to = None  # type: str
    """ (str) Date of renewal end. """

    period_delta = None  # type: int
    """ (int) Size of renewal period. """

    period_uom = None  # type: str
    """ (str) Unit of measure for renewal period. One of: year, month, day, hour. """


class RenewalSchema(BaseSchema):
    from_ = fields.Str(attribute='from')
    to = fields.Str()
    period_delta = fields.Int()
    period_uom = fields.Str()

    @post_load
    def make_object(self, data):
        return Renewal(**data)


class Item(BaseModel):
    """ A product item. """

    mpn = None  # type: str
    """ (str) Item manufacture part number. """

    quantity = None  # type: Union[int, str]
    """ (int|str) Number of items of the type in the asset, or 'unlimited' """

    old_quantity = None  # type: Optional[int]
    """ (int|None) Previous value of quantity. """

    renewal = None  # type: Optional[Renewal]
    """ (:py:class:`.Renewal` | None) Parameters of renewal request
    (empty for all other types).
    """

    global_id = None  # type: str
    """ (str) Global id. """


class ItemSchema(BaseSchema):
    mpn = fields.Str()
    quantity = fields.Str()
    old_quantity = fields.Integer(allow_none=True)
    renewal = fields.Nested(RenewalSchema, allow_none=True)
    global_id = fields.Str()

    @post_load
    def make_object(self, data):
        # If quantity string contains a number, convert to int
        if 'quantity' in data:
            quantity = data['quantity']
            if quantity.isdigit() or (quantity.startswith('-') and quantity[1:].isdigit()):
                data['quantity'] = int(quantity)
        return Item(**data)
