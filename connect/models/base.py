# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import json

from .schemas import BaseSchema


class BaseModel(object):
    """ Base class of all models.

    All the arguments provided on creation of the model are injected as attributes on the object.
    """

    _schema = BaseSchema()  # type: BaseSchema

    id = None  # type: str
    """ (str) Globally unique id. """

    def __init__(self, **kwargs):
        # Inject parsed properties in the model
        for attr, val in kwargs.items():
            setattr(self, attr, val)

    @property
    def json_str(self):
        """
        :return: String with the JSON representation of the model.
        :rtype: str
        """
        return json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))

    @property
    def json(self):
        """
        :return: A list or dictionary with the JSON representation of the model.
        :rtype: dict|list
        """
        return json.loads(self.json_str)

    @classmethod
    def deserialize(cls, json_str):
        """ Deserialize a string containing JSON data into a model.

        :param str json_str: String containing the JSON data to be deserialized.
        :return: An instance of the same class as the receiver of the call, or a list of instances.
        :rtype: Any|list[Any]
        :raises TypeError: Raised if the JSON data cannot be deserialized.
        :raises ValueError: Raised if the string passed is not in JSON format.
        """
        return cls.deserialize_json(json.loads(json_str))

    @classmethod
    def deserialize_json(cls, json_data):
        """ Deserialize JSON data into a model.

        :param dict|list json_data: JSON list or dictionary to be deserialized.
        :return: An instance of the same class as the receiver of the call, or a list of instances.
        :rtype: Any|list[Any]
        :raises TypeError: Raised if the data cannot be deserialized.
        """
        objects, error = cls._schema.load(json_data, many=isinstance(json_data, list))
        if error:
            raise TypeError(
                'Invalid structure for initialization of `{type}`. \n'
                'Error: {error}. \nJSON data: {data}'
                .format(
                    type=cls.__name__,
                    error=error,
                    data=json_data),
            )
        return objects
