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



class DataShortlinkHit(ModelNormal):


    allowed_values = {
        ('device',): {
            'MOBILE': "mobile",
            'TABLET': "tablet",
            'DESKTOP': "desktop",
        },
    }

    validations = {
        ('campaign_id',): {
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
            'hit_id': (int,),  # noqa: E501
            'shortlink_id': (str,),  # noqa: E501
            'url': (str,),  # noqa: E501
            'device': (str,),  # noqa: E501
            'browser': (str,),  # noqa: E501
            'browser_version': (str,),  # noqa: E501
            'os': (str,),  # noqa: E501
            'os_version': (str,),  # noqa: E501
            'brand': (str,),  # noqa: E501
            'model': (str,),  # noqa: E501
            'screen_resolution': (str,),  # noqa: E501
            'accept_language': (str,),  # noqa: E501
            'referrer': (str, none_type,),  # noqa: E501
            'ip_address': (str,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            'city': (str,),  # noqa: E501
            'datetime': (str,),  # noqa: E501
            'phone_number': (str,),  # noqa: E501
            'campaign_id': (str, none_type,),  # noqa: E501
            'group_id': (str, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'hit_id': 'hitId',  # noqa: E501
        'shortlink_id': 'shortlinkId',  # noqa: E501
        'url': 'url',  # noqa: E501
        'device': 'device',  # noqa: E501
        'browser': 'browser',  # noqa: E501
        'browser_version': 'browserVersion',  # noqa: E501
        'os': 'os',  # noqa: E501
        'os_version': 'osVersion',  # noqa: E501
        'brand': 'brand',  # noqa: E501
        'model': 'model',  # noqa: E501
        'screen_resolution': 'screenResolution',  # noqa: E501
        'accept_language': 'acceptLanguage',  # noqa: E501
        'referrer': 'referrer',  # noqa: E501
        'ip_address': 'ipAddress',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        'city': 'city',  # noqa: E501
        'datetime': 'datetime',  # noqa: E501
        'phone_number': 'phoneNumber',  # noqa: E501
        'campaign_id': 'campaignId',  # noqa: E501
        'group_id': 'groupId',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, hit_id, shortlink_id, url, device, browser, browser_version, os, os_version, brand, model, screen_resolution, accept_language, referrer, ip_address, country_iso, city, datetime, *args, **kwargs):  # noqa: E501
        """DataShortlinkHit - a model

        Args:
            hit_id (int):
            shortlink_id (str): ID of the short link
            url (str): URL of the short link
            device (str): Type of device of the visitor
            browser (str): Type of browser of the visitor that accessed the short link
            browser_version (str): Browser version of the device that accessed the short link
            os (str): Operating system of the visitor that accessed the short link (eg. Android, Windows, Linux, etc.)
            os_version (str): Version of the operating system
            brand (str): Brand of phone/tablet of the visitor that accessed the short link
            model (str): Model of phone/tabled of the visitor that accessed the short link (eg. P30 Pro, Galaxy S8, etc.)
            screen_resolution (str):
            accept_language (str):
            referrer (str, none_type):
            ip_address (str): Anonymized IP address without the last byte. Eg. `204.79.200.0`
            country_iso (str): Two-letter country ISO of the visitor that accessed the short link
            city (str): The city of the visitor that accessed the short link
            datetime (str):


            phone_number (str): Phone number of the visitor that made the hit to the shortlink (works if link tracking option is used when sending a message). If short link tracking was enabled, this parameter will not be null. . [optional]  # noqa: E501
            campaign_id (str, none_type): Identifier of the campaign from which the contact has made the visit. If short link tracking was enabled, this parameter will not be null.. [optional]  # noqa: E501
            group_id (str, none_type): Identifier of the group the contact is in. If short link tracking was enabled, this parameter will not be null.. [optional]  # noqa: E501
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

        self.hit_id = hit_id
        self.shortlink_id = shortlink_id
        self.url = url
        self.device = device
        self.browser = browser
        self.browser_version = browser_version
        self.os = os
        self.os_version = os_version
        self.brand = brand
        self.model = model
        self.screen_resolution = screen_resolution
        self.accept_language = accept_language
        self.referrer = referrer
        self.ip_address = ip_address
        self.country_iso = country_iso
        self.city = city
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
    def __init__(self, hit_id, shortlink_id, url, device, browser, browser_version, os, os_version, brand, model, screen_resolution, accept_language, referrer, ip_address, country_iso, city, datetime, *args, **kwargs):  # noqa: E501
        """DataShortlinkHit - a model

        Args:
            hit_id (int):
            shortlink_id (str): ID of the short link
            url (str): URL of the short link
            device (str): Type of device of the visitor
            browser (str): Type of browser of the visitor that accessed the short link
            browser_version (str): Browser version of the device that accessed the short link
            os (str): Operating system of the visitor that accessed the short link (eg. Android, Windows, Linux, etc.)
            os_version (str): Version of the operating system
            brand (str): Brand of phone/tablet of the visitor that accessed the short link
            model (str): Model of phone/tabled of the visitor that accessed the short link (eg. P30 Pro, Galaxy S8, etc.)
            screen_resolution (str):
            accept_language (str):
            referrer (str, none_type):
            ip_address (str): Anonymized IP address without the last byte. Eg. `204.79.200.0`
            country_iso (str): Two-letter country ISO of the visitor that accessed the short link
            city (str): The city of the visitor that accessed the short link
            datetime (str):


            phone_number (str): Phone number of the visitor that made the hit to the shortlink (works if link tracking option is used when sending a message). If short link tracking was enabled, this parameter will not be null. . [optional]  # noqa: E501
            campaign_id (str, none_type): Identifier of the campaign from which the contact has made the visit. If short link tracking was enabled, this parameter will not be null.. [optional]  # noqa: E501
            group_id (str, none_type): Identifier of the group the contact is in. If short link tracking was enabled, this parameter will not be null.. [optional]  # noqa: E501
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

        self.hit_id = hit_id
        self.shortlink_id = shortlink_id
        self.url = url
        self.device = device
        self.browser = browser
        self.browser_version = browser_version
        self.os = os
        self.os_version = os_version
        self.brand = brand
        self.model = model
        self.screen_resolution = screen_resolution
        self.accept_language = accept_language
        self.referrer = referrer
        self.ip_address = ip_address
        self.country_iso = country_iso
        self.city = city
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
