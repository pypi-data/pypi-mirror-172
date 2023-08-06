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


def lazy_import():
    from smscx_client.model.text_analysis import TextAnalysis
    globals()['TextAnalysis'] = TextAnalysis


class DataReports(ModelNormal):


    allowed_values = {
        ('status',): {
            'ACCEPTED': "ACCEPTED",
            'SENT': "SENT",
            'DELIVERED': "DELIVERED",
            'FAILED': "FAILED",
            'SCHEDULED': "SCHEDULED",
            'REJECTED': "REJECTED",
            'NO_COVERAGE': "NO COVERAGE",
        },
        ('source',): {
            'API': "api",
            'WEBAPP': "webapp",
            'SMPP': "smpp",
            'PLUGIN': "plugin",
            'ALERTS': "alerts",
            'EXCEL': "excel",
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
        ('country_iso',): {
            'max_length': 2,
            'min_length': 2,
        },
        ('_from',): {
            'max_length': 15,
            'min_length': 3,
        },
    }

    @cached_property
    def additional_properties_type():
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def api_types():
        """
        Returns
            api_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'msg_id': (str,),  # noqa: E501
            'status': (str,),  # noqa: E501
            'status_code': (int,),  # noqa: E501
            'error_code': (int, none_type,),  # noqa: E501
            'in_quiet_hours': (bool,),  # noqa: E501
            'created_at': (datetime,),  # noqa: E501
            'updated_at': (datetime, none_type,),  # noqa: E501
            'cost': (float,),  # noqa: E501
            'to': (str,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            '_from': (str,),  # noqa: E501
            'source': (str,),  # noqa: E501
            'channel': (str,),  # noqa: E501
            'text': (str,),  # noqa: E501
            'text_analysis': (TextAnalysis,),  # noqa: E501
            'scheduled_at': (datetime, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'msg_id': 'msgId',  # noqa: E501
        'status': 'status',  # noqa: E501
        'status_code': 'statusCode',  # noqa: E501
        'error_code': 'errorCode',  # noqa: E501
        'in_quiet_hours': 'inQuietHours',  # noqa: E501
        'created_at': 'createdAt',  # noqa: E501
        'updated_at': 'updatedAt',  # noqa: E501
        'cost': 'cost',  # noqa: E501
        'to': 'to',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        '_from': 'from',  # noqa: E501
        'source': 'source',  # noqa: E501
        'channel': 'channel',  # noqa: E501
        'text': 'text',  # noqa: E501
        'text_analysis': 'textAnalysis',  # noqa: E501
        'scheduled_at': 'scheduledAt',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, msg_id, status, status_code, error_code, in_quiet_hours, created_at, updated_at, cost, to, country_iso, _from, source, channel, text, text_analysis, *args, **kwargs):  # noqa: E501
        """DataReports - a model

        Args:
            msg_id (str): Unique message identifier
            status (str): Delivery report of the message 
            status_code (int): Status code for the delivery report 
            error_code (int, none_type): Status code for the failed delivery report 
            in_quiet_hours (bool): Specified if the sending was between the saved quiet hours 
            created_at (datetime): Date and time of sending the message
            updated_at (datetime, none_type): Date and time of last delivery report update of the message
            cost (float): The cost of sending a message, in the currency of the account (**eur** or **usd**). It is calculated as ***cost per message part x parts***. Eg. 3 x 0.041 = 0.123  <br>This parameter has value zero (0) if the status of the message is `REJECTED` or `NO COVERAGE` 
            to (str): Destination phone number in E.164 format 
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard of the destinations. Eg. DE, FR, IT
            _from (str): Originator (sender name) of the message 
            source (str): Source of the message sending
            channel (str): Channel that sent the message
            text (str): Content of the message
            text_analysis (TextAnalysis):


            scheduled_at (datetime, none_type): Date and time when the message was scheduled. [optional]  # noqa: E501
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
        self.status = status
        self.status_code = status_code
        self.error_code = error_code
        self.in_quiet_hours = in_quiet_hours
        self.created_at = created_at
        self.updated_at = updated_at
        self.cost = cost
        self.to = to
        self.country_iso = country_iso
        self._from = _from
        self.source = source
        self.channel = channel
        self.text = text
        self.text_analysis = text_analysis
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
    def __init__(self, msg_id, status, status_code, error_code, in_quiet_hours, created_at, updated_at, cost, to, country_iso, _from, source, channel, text, text_analysis, *args, **kwargs):  # noqa: E501
        """DataReports - a model

        Args:
            msg_id (str): Unique message identifier
            status (str): Delivery report of the message 
            status_code (int): Status code for the delivery report 
            error_code (int, none_type): Status code for the failed delivery report 
            in_quiet_hours (bool): Specified if the sending was between the saved quiet hours 
            created_at (datetime): Date and time of sending the message
            updated_at (datetime, none_type): Date and time of last delivery report update of the message
            cost (float): The cost of sending a message, in the currency of the account (**eur** or **usd**). It is calculated as ***cost per message part x parts***. Eg. 3 x 0.041 = 0.123  <br>This parameter has value zero (0) if the status of the message is `REJECTED` or `NO COVERAGE` 
            to (str): Destination phone number in E.164 format 
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard of the destinations. Eg. DE, FR, IT
            _from (str): Originator (sender name) of the message 
            source (str): Source of the message sending
            channel (str): Channel that sent the message
            text (str): Content of the message
            text_analysis (TextAnalysis):


            scheduled_at (datetime, none_type): Date and time when the message was scheduled. [optional]  # noqa: E501
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
        self.status = status
        self.status_code = status_code
        self.error_code = error_code
        self.in_quiet_hours = in_quiet_hours
        self.created_at = created_at
        self.updated_at = updated_at
        self.cost = cost
        self.to = to
        self.country_iso = country_iso
        self._from = _from
        self.source = source
        self.channel = channel
        self.text = text
        self.text_analysis = text_analysis
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
