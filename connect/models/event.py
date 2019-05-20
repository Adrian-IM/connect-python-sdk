# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.
import datetime
from typing import Optional

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema
from .company import User, UserSchema


class EventInfo(BaseModel):
    """ Represents the date and user that caused an event. """

    at = None  # type: Optional[datetime.datetime]
    """ (datetime.datetime|None) Date when the event occurred. """

    by = None  # type: Optional[User]
    """ (:py:class:`.User`) User that caused the event. """


class EventInfoSchema(BaseSchema):
    at = fields.DateTime(allow_none=True)
    by = fields.Nested(UserSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        return EventInfo(**data)


class Events(BaseModel):
    """ Represents a set of events that can take place on an object. """

    created = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Creation event. """

    inquired = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Inquire event. """

    pended = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Pending event. """

    validated = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Validation event. """

    updated = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Update event. """


class EventsSchema(BaseSchema):
    created = fields.Nested(EventInfoSchema)
    inquired = fields.Nested(EventInfoSchema)
    pended = fields.Nested(EventInfoSchema)
    validated = fields.Nested(EventInfoSchema)
    updated = fields.Nested(EventInfoSchema)

    @post_load
    def make_object(self, data):
        return Events(**data)
