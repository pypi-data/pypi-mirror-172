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
    from smscx_client.model.rental_cost import RentalCost
    globals()['RentalCost'] = RentalCost


class DataAvailableNumbersRent(ModelNormal):


    allowed_values = {
        ('sms',): {
            'INBOUND': "inbound",
            'OUTBOUND': "outbound",
        },
        ('min_rent',): {
            'None': None,
            '1': "1",
            '7': "7",
            '30': "30",
        },
        ('max_rent',): {
            'None': None,
            '1': "1",
            '7': "7",
            '30': "30",
        },
    }

    validations = {
        ('number_id',): {
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
            'number_id': (str,),  # noqa: E501
            'phone_number': (str, none_type,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            'network_operator': (str,),  # noqa: E501
            'sms': ([str],),  # noqa: E501
            'voice': ([str],),  # noqa: E501
            'min_rent': (str, none_type,),  # noqa: E501
            'max_rent': (str, none_type,),  # noqa: E501
            'setup_cost': (float,),  # noqa: E501
            'rental_cost': (RentalCost,),  # noqa: E501
            'inbound_sms_cost': (float,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'number_id': 'numberId',  # noqa: E501
        'phone_number': 'phoneNumber',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        'network_operator': 'networkOperator',  # noqa: E501
        'sms': 'sms',  # noqa: E501
        'voice': 'voice',  # noqa: E501
        'min_rent': 'minRent',  # noqa: E501
        'max_rent': 'maxRent',  # noqa: E501
        'setup_cost': 'setupCost',  # noqa: E501
        'rental_cost': 'rentalCost',  # noqa: E501
        'inbound_sms_cost': 'inboundSmsCost',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, number_id, phone_number, country_iso, network_operator, sms, voice, min_rent, max_rent, setup_cost, rental_cost, inbound_sms_cost, *args, **kwargs):  # noqa: E501
        """DataAvailableNumbersRent - a model

        Args:
            number_id (str): Unique identifier of phone number
            phone_number (str, none_type): Phone number in international E.164 format. In some cases this value might be null as the phone number will be selected random from a pool of numbers
            country_iso (str): Two-letter country ISO of the phone number
            network_operator (str): Network operator of the phone number
            sms ([str]): SMS features that the phone number supports (inbound or outbound SMS)
            voice ([str]): Voice features that the phone number supports
            min_rent (str, none_type): Minimum period that this phone number must be rented (in days)
            max_rent (str, none_type): Maximum period that this phone number can be rented (in days)
            setup_cost (float): One time setup fee for the rented phone number (if applicable)
            rental_cost (RentalCost):
            inbound_sms_cost (float): Cost for receiving a SMS on this phone number (most of the time receiving is free, meaning this is has value 0)


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

        self.number_id = number_id
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.network_operator = network_operator
        self.sms = sms
        self.voice = voice
        self.min_rent = min_rent
        self.max_rent = max_rent
        self.setup_cost = setup_cost
        self.rental_cost = rental_cost
        self.inbound_sms_cost = inbound_sms_cost
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
    def __init__(self, number_id, phone_number, country_iso, network_operator, sms, voice, min_rent, max_rent, setup_cost, rental_cost, inbound_sms_cost, *args, **kwargs):  # noqa: E501
        """DataAvailableNumbersRent - a model

        Args:
            number_id (str): Unique identifier of phone number
            phone_number (str, none_type): Phone number in international E.164 format. In some cases this value might be null as the phone number will be selected random from a pool of numbers
            country_iso (str): Two-letter country ISO of the phone number
            network_operator (str): Network operator of the phone number
            sms ([str]): SMS features that the phone number supports (inbound or outbound SMS)
            voice ([str]): Voice features that the phone number supports
            min_rent (str, none_type): Minimum period that this phone number must be rented (in days)
            max_rent (str, none_type): Maximum period that this phone number can be rented (in days)
            setup_cost (float): One time setup fee for the rented phone number (if applicable)
            rental_cost (RentalCost):
            inbound_sms_cost (float): Cost for receiving a SMS on this phone number (most of the time receiving is free, meaning this is has value 0)


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

        self.number_id = number_id
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.network_operator = network_operator
        self.sms = sms
        self.voice = voice
        self.min_rent = min_rent
        self.max_rent = max_rent
        self.setup_cost = setup_cost
        self.rental_cost = rental_cost
        self.inbound_sms_cost = inbound_sms_cost
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
