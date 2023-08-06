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


class InfoRentNumber(ModelNormal):


    allowed_values = {
        ('rent_period',): {
            '1': 1,
            '7': 7,
            '30': 30,
        },
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
        ('rent_id',): {
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
            'rent_id': (str,),  # noqa: E501
            'rent_cost': (float,),  # noqa: E501
            'setup_cost': (float,),  # noqa: E501
            'rent_period': (int,),  # noqa: E501
            'rent_start': (datetime,),  # noqa: E501
            'rent_end': (datetime,),  # noqa: E501
            'phone_number': (str,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            'network_operator': (str,),  # noqa: E501
            'auto_renew': (bool,),  # noqa: E501
            'sms': ([str],),  # noqa: E501
            'voice': ([str],),  # noqa: E501
            'min_rent': (str, none_type,),  # noqa: E501
            'max_rent': (str, none_type,),  # noqa: E501
            'rental_cost': (RentalCost,),  # noqa: E501
            'inbound_sms_cost': (float,),  # noqa: E501
            'callback_url': (str, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'rent_id': 'rentId',  # noqa: E501
        'rent_cost': 'rentCost',  # noqa: E501
        'setup_cost': 'setupCost',  # noqa: E501
        'rent_period': 'rentPeriod',  # noqa: E501
        'rent_start': 'rentStart',  # noqa: E501
        'rent_end': 'rentEnd',  # noqa: E501
        'phone_number': 'phoneNumber',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        'network_operator': 'networkOperator',  # noqa: E501
        'auto_renew': 'autoRenew',  # noqa: E501
        'sms': 'sms',  # noqa: E501
        'voice': 'voice',  # noqa: E501
        'min_rent': 'minRent',  # noqa: E501
        'max_rent': 'maxRent',  # noqa: E501
        'rental_cost': 'rentalCost',  # noqa: E501
        'inbound_sms_cost': 'inboundSmsCost',  # noqa: E501
        'callback_url': 'callbackUrl',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, rent_id, rent_cost, setup_cost, rent_period, rent_start, rent_end, phone_number, country_iso, network_operator, auto_renew, sms, voice, min_rent, max_rent, rental_cost, inbound_sms_cost, callback_url, *args, **kwargs):  # noqa: E501
        """InfoRentNumber - a model

        Args:
            rent_id (str): Unique identifier of the rent operation
            rent_cost (float): Cost of renting the phone number for the period chosen
            setup_cost (float): One time setup fee for the rented phone number (if applicable)
            rent_period (int): Rental period of the phone number (in days)
            rent_start (datetime): Start date and time of the rental period (UTC)
            rent_end (datetime): End date and time of the rental period (UTC)
            phone_number (str): Phone number that is rented in international E.164 format
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard. Eg. `DE`, `FR`, `IT`
            network_operator (str): Network operator of the phone number
            auto_renew (bool): Status of the auto renewal setting for this number rental
            sms ([str]): SMS features that the phone number supports (inbound or outbound SMS)
            voice ([str]): Voice features that the phone number supports
            min_rent (str, none_type): Minimum period that this phone number must be rented (in days)
            max_rent (str, none_type): Maximum period that this phone number can be rented (in days)
            rental_cost (RentalCost):
            inbound_sms_cost (float): Cost for receiving a SMS on this phone number (most of the time receiving is free, meaning this is has value 0)
            callback_url (str, none_type): Callback URL (or webhook) to get the received SMS on the rented phone number


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

        self.rent_id = rent_id
        self.rent_cost = rent_cost
        self.setup_cost = setup_cost
        self.rent_period = rent_period
        self.rent_start = rent_start
        self.rent_end = rent_end
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.network_operator = network_operator
        self.auto_renew = auto_renew
        self.sms = sms
        self.voice = voice
        self.min_rent = min_rent
        self.max_rent = max_rent
        self.rental_cost = rental_cost
        self.inbound_sms_cost = inbound_sms_cost
        self.callback_url = callback_url
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
    def __init__(self, rent_id, rent_cost, setup_cost, rent_period, rent_start, rent_end, phone_number, country_iso, network_operator, auto_renew, sms, voice, min_rent, max_rent, rental_cost, inbound_sms_cost, callback_url, *args, **kwargs):  # noqa: E501
        """InfoRentNumber - a model

        Args:
            rent_id (str): Unique identifier of the rent operation
            rent_cost (float): Cost of renting the phone number for the period chosen
            setup_cost (float): One time setup fee for the rented phone number (if applicable)
            rent_period (int): Rental period of the phone number (in days)
            rent_start (datetime): Start date and time of the rental period (UTC)
            rent_end (datetime): End date and time of the rental period (UTC)
            phone_number (str): Phone number that is rented in international E.164 format
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard. Eg. `DE`, `FR`, `IT`
            network_operator (str): Network operator of the phone number
            auto_renew (bool): Status of the auto renewal setting for this number rental
            sms ([str]): SMS features that the phone number supports (inbound or outbound SMS)
            voice ([str]): Voice features that the phone number supports
            min_rent (str, none_type): Minimum period that this phone number must be rented (in days)
            max_rent (str, none_type): Maximum period that this phone number can be rented (in days)
            rental_cost (RentalCost):
            inbound_sms_cost (float): Cost for receiving a SMS on this phone number (most of the time receiving is free, meaning this is has value 0)
            callback_url (str, none_type): Callback URL (or webhook) to get the received SMS on the rented phone number


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

        self.rent_id = rent_id
        self.rent_cost = rent_cost
        self.setup_cost = setup_cost
        self.rent_period = rent_period
        self.rent_start = rent_start
        self.rent_end = rent_end
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.network_operator = network_operator
        self.auto_renew = auto_renew
        self.sms = sms
        self.voice = voice
        self.min_rent = min_rent
        self.max_rent = max_rent
        self.rental_cost = rental_cost
        self.inbound_sms_cost = inbound_sms_cost
        self.callback_url = callback_url
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
