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



class DataShortlinkDetail(ModelNormal):
    """
    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
        ('device',): {
            'None': None,
            'MOBILE': "mobile",
            'TABLET': "tablet",
            'DESKTOP': "desktop",
        },
    }

    validations = {
        ('phone_number_country_iso',): {
            'max_length': 2,
            'min_length': 2,
        },
        ('campaign_id',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
        },
    }

    additional_properties_type = None

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
            'device': (str, none_type,),  # noqa: E501
            'browser': (str, none_type,),  # noqa: E501
            'browser_version': (str, none_type,),  # noqa: E501
            'os': (str, none_type,),  # noqa: E501
            'os_version': (str, none_type,),  # noqa: E501
            'brand': (str, none_type,),  # noqa: E501
            'model': (str, none_type,),  # noqa: E501
            'screen_resolution': (str, none_type,),  # noqa: E501
            'accept_language': (str, none_type,),  # noqa: E501
            'referrer': (str, none_type,),  # noqa: E501
            'ip_address': (str, none_type,),  # noqa: E501
            'country_iso': (str, none_type,),  # noqa: E501
            'city': (str, none_type,),  # noqa: E501
            'datetime': (str,),  # noqa: E501
            'phone_number': (str, none_type,),  # noqa: E501
            'phone_number_country_iso': (str, none_type,),  # noqa: E501
            'campaign_id': (str, none_type,),  # noqa: E501
            'group_id': (str, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'hit_id': 'hitId',  # noqa: E501
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
        'phone_number_country_iso': 'phoneNumberCountryIso',  # noqa: E501
        'campaign_id': 'campaignId',  # noqa: E501
        'group_id': 'groupId',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, hit_id, device, browser, browser_version, os, os_version, brand, model, screen_resolution, accept_language, referrer, ip_address, country_iso, city, datetime, *args, **kwargs):  # noqa: E501
        """DataShortlinkDetail - a model

        Args:
            hit_id (int):
            device (str, none_type): Type of device of the visitor
            browser (str, none_type): Type of browser of the visitor that accessed the short link
            browser_version (str, none_type): Browser version of the device that accessed the short link
            os (str, none_type): Operating system of the visitor that accessed the short link (eg. Android, Windows, Linux, etc.)
            os_version (str, none_type): Version of the operating system
            brand (str, none_type): Brand of phone/tablet of the visitor that accessed the short link
            model (str, none_type): Model of phone/tabled of the visitor that accessed the short link (eg. P30 Pro, Galaxy S8, etc.)
            screen_resolution (str, none_type):
            accept_language (str, none_type):
            referrer (str, none_type):
            ip_address (str, none_type): Anonymized IP address without the last byte. Eg. `204.79.200.0`
            country_iso (str, none_type): Two-letter country ISO of the visitor that accessed the short link
            city (str, none_type): The city of the visitor that accessed the short link
            datetime (str):

        Keyword Args:
            _check_type (bool): if True, values for parameters in api_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names,.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            phone_number (str, none_type): Phone number of the visitor that made the hit to the shortlink (works if link tracking option is used when sending a message). If short link tracking was enabled, this parameter will not be null. . [optional]  # noqa: E501
            phone_number_country_iso (str, none_type): The country code of the phone number in ISO-3166 alpha 2 format (eg. DE, IT, FR). [optional]  # noqa: E501
            campaign_id (str, none_type): Identifier of the campaign from which the contact has unsubscribed. If short link tracking was enabled, this parameter will not be null.. [optional]  # noqa: E501
            group_id (str, none_type): Identifier of the group the contact was in. If short link tracking was enabled, this parameter will not be null.. [optional]  # noqa: E501
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
    def __init__(self, hit_id, device, browser, browser_version, os, os_version, brand, model, screen_resolution, accept_language, referrer, ip_address, country_iso, city, datetime, *args, **kwargs):  # noqa: E501
        """DataShortlinkDetail - a model

        Args:
            hit_id (int):
            device (str, none_type): Type of device of the visitor
            browser (str, none_type): Type of browser of the visitor that accessed the short link
            browser_version (str, none_type): Browser version of the device that accessed the short link
            os (str, none_type): Operating system of the visitor that accessed the short link (eg. Android, Windows, Linux, etc.)
            os_version (str, none_type): Version of the operating system
            brand (str, none_type): Brand of phone/tablet of the visitor that accessed the short link
            model (str, none_type): Model of phone/tabled of the visitor that accessed the short link (eg. P30 Pro, Galaxy S8, etc.)
            screen_resolution (str, none_type):
            accept_language (str, none_type):
            referrer (str, none_type):
            ip_address (str, none_type): Anonymized IP address without the last byte. Eg. `204.79.200.0`
            country_iso (str, none_type): Two-letter country ISO of the visitor that accessed the short link
            city (str, none_type): The city of the visitor that accessed the short link
            datetime (str):

        Keyword Args:
            _check_type (bool): if True, values for parameters in api_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names,.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            phone_number (str, none_type): Phone number of the visitor that made the hit to the shortlink (works if link tracking option is used when sending a message). If short link tracking was enabled, this parameter will not be null. . [optional]  # noqa: E501
            phone_number_country_iso (str, none_type): The country code of the phone number in ISO-3166 alpha 2 format (eg. DE, IT, FR). [optional]  # noqa: E501
            campaign_id (str, none_type): Identifier of the campaign from which the contact has unsubscribed. If short link tracking was enabled, this parameter will not be null.. [optional]  # noqa: E501
            group_id (str, none_type): Identifier of the group the contact was in. If short link tracking was enabled, this parameter will not be null.. [optional]  # noqa: E501
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
