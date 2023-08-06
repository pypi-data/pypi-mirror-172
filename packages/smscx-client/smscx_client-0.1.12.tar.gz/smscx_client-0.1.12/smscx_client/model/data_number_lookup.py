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
    from smscx_client.model.original_network import OriginalNetwork
    from smscx_client.model.ported_network import PortedNetwork
    from smscx_client.model.roaming_network import RoamingNetwork
    globals()['OriginalNetwork'] = OriginalNetwork
    globals()['PortedNetwork'] = PortedNetwork
    globals()['RoamingNetwork'] = RoamingNetwork


class DataNumberLookup(ModelNormal):


    allowed_values = {
        ('status',): {
            'ACTIVE': "ACTIVE",
            'ABSENT': "ABSENT",
            'BARRED': "BARRED",
            'UNKNOWN': "UNKNOWN",
            'FAILED': "FAILED",
        },
    }

    validations = {
        ('lookup_id',): {
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
            'phone_number': (str,),  # noqa: E501
            'lookup_id': (str,),  # noqa: E501
            'cost': (float,),  # noqa: E501
            'mcc': (str,),  # noqa: E501
            'mccmnc': (str,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            'country_name': (str,),  # noqa: E501
            'country_name_locale': (str,),  # noqa: E501
            'status': (str,),  # noqa: E501
            'status_description': (str,),  # noqa: E501
            'ported': (bool,),  # noqa: E501
            'roaming': (bool,),  # noqa: E501
            'original_network': (OriginalNetwork,),  # noqa: E501
            'ported_network': (PortedNetwork,),  # noqa: E501
            'roaming_network': (RoamingNetwork,),  # noqa: E501
            'datetime': (datetime,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'phone_number': 'phoneNumber',  # noqa: E501
        'lookup_id': 'lookupId',  # noqa: E501
        'cost': 'cost',  # noqa: E501
        'mcc': 'mcc',  # noqa: E501
        'mccmnc': 'mccmnc',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        'country_name': 'countryName',  # noqa: E501
        'country_name_locale': 'countryNameLocale',  # noqa: E501
        'status': 'status',  # noqa: E501
        'status_description': 'statusDescription',  # noqa: E501
        'ported': 'ported',  # noqa: E501
        'roaming': 'roaming',  # noqa: E501
        'original_network': 'originalNetwork',  # noqa: E501
        'ported_network': 'portedNetwork',  # noqa: E501
        'roaming_network': 'roamingNetwork',  # noqa: E501
        'datetime': 'datetime',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, phone_number, lookup_id, cost, mcc, mccmnc, country_iso, country_name, country_name_locale, status, status_description, ported, roaming, original_network, ported_network, roaming_network, datetime, *args, **kwargs):  # noqa: E501
        """DataNumberLookup - a model

        Args:
            phone_number (str): Phone number in international E.164 format
            lookup_id (str): Unique lookup identifier
            cost (float): The cost of phone number lookup
            mcc (str): Mobile country code. [See full list of MCC](https://www.itu.int/dms_pub/itu-t/opb/sp/T-SP-E.212B-2018-PDF-E.pdf)
            mccmnc (str): Mobile country code + Mobile network code. [See full list of MCC + MNC](https://www.itu.int/dms_pub/itu-t/opb/sp/T-SP-E.212B-2018-PDF-E.pdf)
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard of the destinations. Eg. `DE`, `FR`, `IT`
            country_name (str): Name of the country of the phone number
            country_name_locale (str): Name of the country in local language
            status (str): Status of the phone number
            status_description (str): Short description of the status
            ported (bool): Returns `true` if the phone number is ported to other mobile network, `false` otherwise
            roaming (bool): Returns `true` if the phone number is roaming in other network, `false` otherwise
            original_network (OriginalNetwork):
            ported_network (PortedNetwork):
            roaming_network (RoamingNetwork):
            datetime (datetime): Date and time of the phone number lookup request


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

        self.phone_number = phone_number
        self.lookup_id = lookup_id
        self.cost = cost
        self.mcc = mcc
        self.mccmnc = mccmnc
        self.country_iso = country_iso
        self.country_name = country_name
        self.country_name_locale = country_name_locale
        self.status = status
        self.status_description = status_description
        self.ported = ported
        self.roaming = roaming
        self.original_network = original_network
        self.ported_network = ported_network
        self.roaming_network = roaming_network
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
    def __init__(self, phone_number, lookup_id, cost, mcc, mccmnc, country_iso, country_name, country_name_locale, status, status_description, ported, roaming, original_network, ported_network, roaming_network, datetime, *args, **kwargs):  # noqa: E501
        """DataNumberLookup - a model

        Args:
            phone_number (str): Phone number in international E.164 format
            lookup_id (str): Unique lookup identifier
            cost (float): The cost of phone number lookup
            mcc (str): Mobile country code. [See full list of MCC](https://www.itu.int/dms_pub/itu-t/opb/sp/T-SP-E.212B-2018-PDF-E.pdf)
            mccmnc (str): Mobile country code + Mobile network code. [See full list of MCC + MNC](https://www.itu.int/dms_pub/itu-t/opb/sp/T-SP-E.212B-2018-PDF-E.pdf)
            country_iso (str): Two-letter country code in ISO-3166 alpha 2 standard of the destinations. Eg. `DE`, `FR`, `IT`
            country_name (str): Name of the country of the phone number
            country_name_locale (str): Name of the country in local language
            status (str): Status of the phone number
            status_description (str): Short description of the status
            ported (bool): Returns `true` if the phone number is ported to other mobile network, `false` otherwise
            roaming (bool): Returns `true` if the phone number is roaming in other network, `false` otherwise
            original_network (OriginalNetwork):
            ported_network (PortedNetwork):
            roaming_network (RoamingNetwork):
            datetime (datetime): Date and time of the phone number lookup request


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

        self.phone_number = phone_number
        self.lookup_id = lookup_id
        self.cost = cost
        self.mcc = mcc
        self.mccmnc = mccmnc
        self.country_iso = country_iso
        self.country_name = country_name
        self.country_name_locale = country_name_locale
        self.status = status
        self.status_description = status_description
        self.ported = ported
        self.roaming = roaming
        self.original_network = original_network
        self.ported_network = ported_network
        self.roaming_network = roaming_network
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
