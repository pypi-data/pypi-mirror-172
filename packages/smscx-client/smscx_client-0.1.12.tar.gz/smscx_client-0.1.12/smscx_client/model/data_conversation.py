import re  # noqa: F401
import sys  # noqa: F401

from smscx_client.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    ApiModel
)
from smscx_client.exceptions import ApiAttributeError



class DataConversation(ModelNormal):


    allowed_values = {
        ('type',): {
            'SENT': "sent",
            'RECEIVED': "received",
        },
        ('status',): {
            'DELIVERED': "DELIVERED",
            'SENT': "SENT",
            'FAILED': "FAILED",
            'SCHEDULED': "SCHEDULED",
        },
        ('channel',): {
            'SMS': "sms",
            'VIBER': "viber",
            'WHATSAPP': "whatsapp",
        },
    }

    validations = {
        ('msg_id',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
        },
    }

    @cached_property
    def additional_properties_type():
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def api_types():
        """
        Returns
            api_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            'msg_id': (str,),  # noqa: E501
            'type': (str,),  # noqa: E501
            'text': (str,),  # noqa: E501
            'rich_media': ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},),  # noqa: E501
            'status': (str,),  # noqa: E501
            'cost': (float,),  # noqa: E501
            'channel': (str,),  # noqa: E501
            'datetime': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'msg_id': 'msgId',  # noqa: E501
        'type': 'type',  # noqa: E501
        'text': 'text',  # noqa: E501
        'rich_media': 'richMedia',  # noqa: E501
        'status': 'status',  # noqa: E501
        'cost': 'cost',  # noqa: E501
        'channel': 'channel',  # noqa: E501
        'datetime': 'datetime',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, msg_id, type, text, rich_media, status, cost, channel, datetime, *args, **kwargs):  # noqa: E501
        """DataConversation - a model

        Args:
            msg_id (str): Unique identifier of the message
            type (str): Direction of the message: sent, received
            text (str): Text message
            rich_media ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}):
            status (str): Delivery report of the message
            cost (float): Cost of the message
            channel (str):
            datetime (str): Date time of the sent/received message


        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', True)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(ApiModel, cls).__new__(cls)

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.msg_id = msg_id
        self.type = type
        self.text = text
        self.rich_media = rich_media
        self.status = status
        self.cost = cost
        self.channel = channel
        self.datetime = datetime
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, msg_id, type, text, rich_media, status, cost, channel, datetime, *args, **kwargs):  # noqa: E501
        """DataConversation - a model

        Args:
            msg_id (str): Unique identifier of the message
            type (str): Direction of the message: sent, received
            text (str): Text message
            rich_media ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}):
            status (str): Delivery report of the message
            cost (float): Cost of the message
            channel (str):
            datetime (str): Date time of the sent/received message


        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.msg_id = msg_id
        self.type = type
        self.text = text
        self.rich_media = rich_media
        self.status = status
        self.cost = cost
        self.channel = channel
        self.datetime = datetime
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_api_data` to instantiate "
                                     f"class with read only attributes.")
