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



class DataOtp(ModelNormal):


    allowed_values = {
        ('status',): {
            'PENDING': "PENDING",
            'VERIFIED': "VERIFIED",
            'EXPIRED': "EXPIRED",
            'CANCELLED': "CANCELLED",
            'FAILED': "FAILED",
        },
    }

    validations = {
        ('otp_id',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
        },
        ('track_id',): {
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
        ('parts',): {
            'inclusive_minimum': 1,
        },
        ('max_attempts',): {
            'inclusive_maximum': 10,
            'inclusive_minimum': 1,
        },
        ('attempts',): {
            'inclusive_maximum': 10,
            'inclusive_minimum': 0,
        },
        ('ttl',): {
            'inclusive_maximum': 1800,
            'inclusive_minimum': 60,
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
            'otp_id': (str,),  # noqa: E501
            'track_id': (str, none_type,),  # noqa: E501
            'phone_number': (str,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            'status': (str,),  # noqa: E501
            'cost': (float,),  # noqa: E501
            'parts': (int,),  # noqa: E501
            'max_attempts': (int,),  # noqa: E501
            'attempts': (int,),  # noqa: E501
            'ttl': (int,),  # noqa: E501
            'otp_callback_url': (str, none_type,),  # noqa: E501
            'date_created': (datetime,),  # noqa: E501
            'date_expires': (datetime,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'otp_id': 'otpId',  # noqa: E501
        'track_id': 'trackId',  # noqa: E501
        'phone_number': 'phoneNumber',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        'status': 'status',  # noqa: E501
        'cost': 'cost',  # noqa: E501
        'parts': 'parts',  # noqa: E501
        'max_attempts': 'maxAttempts',  # noqa: E501
        'attempts': 'attempts',  # noqa: E501
        'ttl': 'ttl',  # noqa: E501
        'otp_callback_url': 'otpCallbackUrl',  # noqa: E501
        'date_created': 'dateCreated',  # noqa: E501
        'date_expires': 'dateExpires',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, otp_id, track_id, phone_number, country_iso, status, cost, parts, max_attempts, attempts, ttl, otp_callback_url, date_created, date_expires, *args, **kwargs):  # noqa: E501
        """DataOtp - a model

        Args:
            otp_id (str): Unique identifier of the OTP request
            track_id (str, none_type): Client provided UUID (v1-v5) for tracking purposes
            phone_number (str): The phone number where the pin was sent    
            country_iso (str): The country ISO of the phone numver. Eg. `DE`, `FR`, `IT`
            status (str): Status of the OTP request. The initial status is `PENDING`
            cost (float): The cost of the OTP request
            parts (int): Message parts
            max_attempts (int): Number of attempts to allow the OTP to be verified before marking it as failed
            attempts (int): Number of unsuccessful attempts made to validate the pin
            ttl (int): The time to live (ttl) defines the time in seconds that a pin is valid. Min 1 minute (60 seconds) and max 30 minutes (1800 seconds)
            otp_callback_url (str, none_type): The webhook where request will be made with status updates for the OTP validation
            date_created (datetime): Datetime of the OTP request
            date_expires (datetime): Datetime of the OTP request expiration. After this date and time the pin will no longer be valid


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

        self.otp_id = otp_id
        self.track_id = track_id
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.status = status
        self.cost = cost
        self.parts = parts
        self.max_attempts = max_attempts
        self.attempts = attempts
        self.ttl = ttl
        self.otp_callback_url = otp_callback_url
        self.date_created = date_created
        self.date_expires = date_expires
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
    def __init__(self, otp_id, track_id, phone_number, country_iso, status, cost, parts, max_attempts, attempts, ttl, otp_callback_url, date_created, date_expires, *args, **kwargs):  # noqa: E501
        """DataOtp - a model

        Args:
            otp_id (str): Unique identifier of the OTP request
            track_id (str, none_type): Client provided UUID (v1-v5) for tracking purposes
            phone_number (str): The phone number where the pin was sent    
            country_iso (str): The country ISO of the phone numver. Eg. `DE`, `FR`, `IT`
            status (str): Status of the OTP request. The initial status is `PENDING`
            cost (float): The cost of the OTP request
            parts (int): Message parts
            max_attempts (int): Number of attempts to allow the OTP to be verified before marking it as failed
            attempts (int): Number of unsuccessful attempts made to validate the pin
            ttl (int): The time to live (ttl) defines the time in seconds that a pin is valid. Min 1 minute (60 seconds) and max 30 minutes (1800 seconds)
            otp_callback_url (str, none_type): The webhook where request will be made with status updates for the OTP validation
            date_created (datetime): Datetime of the OTP request
            date_expires (datetime): Datetime of the OTP request expiration. After this date and time the pin will no longer be valid


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

        self.otp_id = otp_id
        self.track_id = track_id
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.status = status
        self.cost = cost
        self.parts = parts
        self.max_attempts = max_attempts
        self.attempts = attempts
        self.ttl = ttl
        self.otp_callback_url = otp_callback_url
        self.date_created = date_created
        self.date_expires = date_expires
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
