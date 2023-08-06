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



class DataWhatsapp(ModelNormal):


    allowed_values = {
        ('status',): {
            'ACCEPTED': "ACCEPTED",
            'SCHEDULED': "SCHEDULED",
            'REJECTED': "REJECTED",
            'NO_COVERAGE': "NO COVERAGE",
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
        ('parts',): {
            'inclusive_maximum': 1,
            'inclusive_minimum': 1,
        },
        ('track_data',): {
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
            'status': (str,),  # noqa: E501
            'status_code': (int,),  # noqa: E501
            'error_code': (int, none_type,),  # noqa: E501
            'created_at': (datetime,),  # noqa: E501
            'in_quiet_hours': (bool,),  # noqa: E501
            'cost': (float,),  # noqa: E501
            'to': (str,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            '_from': (str,),  # noqa: E501
            'text': (str,),  # noqa: E501
            'parts': (int,),  # noqa: E501
            'track_data': (str,),  # noqa: E501
            'scheduled_at': (datetime,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'msg_id': 'msgId',  # noqa: E501
        'status': 'status',  # noqa: E501
        'status_code': 'statusCode',  # noqa: E501
        'error_code': 'errorCode',  # noqa: E501
        'created_at': 'createdAt',  # noqa: E501
        'in_quiet_hours': 'inQuietHours',  # noqa: E501
        'cost': 'cost',  # noqa: E501
        'to': 'to',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        '_from': 'from',  # noqa: E501
        'text': 'text',  # noqa: E501
        'parts': 'parts',  # noqa: E501
        'track_data': 'trackData',  # noqa: E501
        'scheduled_at': 'scheduledAt',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, msg_id, status, status_code, error_code, created_at, in_quiet_hours, cost, to, country_iso, _from, text, parts, *args, **kwargs):  # noqa: E501
        """DataWhatsapp - a model

        Args:
            msg_id (str): Unique message identifier needed to track the delivery report
            status (str): Possible status of the message at request time:  * `ACCEPTED` - Message has been accepted for delivery  * `SCHEDULED` - Message has been scheduled at the date time specified  * `REJECTED` - Message was rejected because the number has opted out from receiving messages (no balance deduction, cost zero)  * `NO COVERAGE` - There is no coverage for this destination, no pricing is set (no balance deduction, cost zero)   The final delivery report (DELIVERED, FAILED) will be sent to the URL provided in the `dlrCallbackUrl` parameter or you can query the status at the resource GET `/reports/single/{msgId}` 
            status_code (int): Status code for the delivery report 
            error_code (int, none_type): Status code for the failed delivery report 
            created_at (datetime): Date and time of sending the message
            in_quiet_hours (bool): If the date of send or the schedule date of a message is detected to be in the quiet hours of the destination phone number, this parameter will be set to `true`. This parameter is `false` if no quiet hours detected
            cost (float): The cost of sending a message, in the currency of the account (**eur** or **usd**). 
            to (str): Destination phone number in E.164 format 
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard of the destinations. Eg. DE, FR, IT
            _from (str): Originator (sender name) of the message 
            text (str): The text message sent with all the fields/variables replaced (if any).
            parts (int): Message parts. For Viber/Whatsapp/Multichannel this variable is always with value 1


            track_data (str): Client own UUID (v1-v5) provided to track messages. [optional]  # noqa: E501
            scheduled_at (datetime): Date and time when the Whatsapp message was scheduled. If the date and time of sending or scheduling is detected to be in the quiet hours interval, the API will schedule the sending of the Whatsapp message at the end of the quiet hours. Eg. If quiet hours is defined between 21:30 and 09:30 and the message sending is at 21:55, then the API will schedule the message the next day at 09:31. [optional]  # noqa: E501
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
        self.created_at = created_at
        self.in_quiet_hours = in_quiet_hours
        self.cost = cost
        self.to = to
        self.country_iso = country_iso
        self._from = _from
        self.text = text
        self.parts = parts
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
    def __init__(self, msg_id, status, status_code, error_code, created_at, in_quiet_hours, cost, to, country_iso, _from, text, parts, *args, **kwargs):  # noqa: E501
        """DataWhatsapp - a model

        Args:
            msg_id (str): Unique message identifier needed to track the delivery report
            status (str): Possible status of the message at request time:  * `ACCEPTED` - Message has been accepted for delivery  * `SCHEDULED` - Message has been scheduled at the date time specified  * `REJECTED` - Message was rejected because the number has opted out from receiving messages (no balance deduction, cost zero)  * `NO COVERAGE` - There is no coverage for this destination, no pricing is set (no balance deduction, cost zero)   The final delivery report (DELIVERED, FAILED) will be sent to the URL provided in the `dlrCallbackUrl` parameter or you can query the status at the resource GET `/reports/single/{msgId}` 
            status_code (int): Status code for the delivery report 
            error_code (int, none_type): Status code for the failed delivery report 
            created_at (datetime): Date and time of sending the message
            in_quiet_hours (bool): If the date of send or the schedule date of a message is detected to be in the quiet hours of the destination phone number, this parameter will be set to `true`. This parameter is `false` if no quiet hours detected
            cost (float): The cost of sending a message, in the currency of the account (**eur** or **usd**). 
            to (str): Destination phone number in E.164 format 
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard of the destinations. Eg. DE, FR, IT
            _from (str): Originator (sender name) of the message 
            text (str): The text message sent with all the fields/variables replaced (if any).
            parts (int): Message parts. For Viber/Whatsapp/Multichannel this variable is always with value 1


            track_data (str): Client own UUID (v1-v5) provided to track messages. [optional]  # noqa: E501
            scheduled_at (datetime): Date and time when the Whatsapp message was scheduled. If the date and time of sending or scheduling is detected to be in the quiet hours interval, the API will schedule the sending of the Whatsapp message at the end of the quiet hours. Eg. If quiet hours is defined between 21:30 and 09:30 and the message sending is at 21:55, then the API will schedule the message the next day at 09:31. [optional]  # noqa: E501
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
        self.created_at = created_at
        self.in_quiet_hours = in_quiet_hours
        self.cost = cost
        self.to = to
        self.country_iso = country_iso
        self._from = _from
        self.text = text
        self.parts = parts
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
