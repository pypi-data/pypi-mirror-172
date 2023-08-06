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
    pass
    #from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
    #globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry


class InfoOptoutsNew(ModelNormal):


    allowed_values = {
    }

    validations = {
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
            'total_valid': (int,),  # noqa: E501
            'total_invalid': (int,),  # noqa: E501
            'total_duplicates': (int,),  # noqa: E501
            'total_phone_numbers': (int,),  # noqa: E501
            #'phone_numbers_by_country': (PhoneNumbersByCountry,),  # noqa: E501
            'invalid': ([str],),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'total_valid': 'totalValid',  # noqa: E501
        'total_invalid': 'totalInvalid',  # noqa: E501
        'total_duplicates': 'totalDuplicates',  # noqa: E501
        'total_phone_numbers': 'totalPhoneNumbers',  # noqa: E501
        #'phone_numbers_by_country': 'phoneNumbersByCountry',  # noqa: E501
        'invalid': 'invalid',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, total_valid, total_invalid, total_duplicates, total_phone_numbers, invalid, *args, **kwargs):  # noqa: E501
        """InfoOptoutsNew - a model

        Args:
            total_valid (int):
            total_invalid (int):
            total_duplicates (int):
            total_phone_numbers (int):
            #phone_numbers_by_country (PhoneNumbersByCountry):
            invalid ([str]): 


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

        self.total_valid = total_valid
        self.total_invalid = total_invalid
        self.total_duplicates = total_duplicates
        self.total_phone_numbers = total_phone_numbers
        #self.phone_numbers_by_country = phone_numbers_by_country
        self.invalid = invalid
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
    def __init__(self, total_valid, total_invalid, total_duplicates, total_phone_numbers, invalid, *args, **kwargs):  # noqa: E501
        """InfoOptoutsNew - a model

        Args:
            total_valid (int):
            total_invalid (int):
            total_duplicates (int):
            total_phone_numbers (int):
            #phone_numbers_by_country (PhoneNumbersByCountry):
            invalid ([str]): 


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

        self.total_valid = total_valid
        self.total_invalid = total_invalid
        self.total_duplicates = total_duplicates
        self.total_phone_numbers = total_phone_numbers
        #self.phone_numbers_by_country = phone_numbers_by_country
        self.invalid = invalid
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
