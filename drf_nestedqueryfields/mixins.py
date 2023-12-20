import re

from django.conf import settings

from rest_framework import serializers


class NestedQueryFieldsMixin(object):
    # If using Django filters in the API, these labels mustn't conflict with any model field names.
    include_arg_name = "fields"
    exclude_arg_name = "fields!"

    # Split field names by this string. It doesn't necessarily have to be a single character.
    # Avoid RFC 1738 reserved characters i.e. ';', '/', '?', ':', '@', '=' and '&'
    delimiter = ","

    def __init__(self, *args, **kwargs):
        super(NestedQueryFieldsMixin, self).__init__(*args, **kwargs)
        self.include_arg_name = getattr(
            settings,
            "DRF_NESTEDQUERYFIELDS_INCLUDE_ARG_NAME",
            self.include_arg_name,
        )
        self.exclude_arg_name = getattr(
            settings,
            "DRF_NESTEDQUERYFIELDS_EXCLUDE_ARG_NAME",
            self.exclude_arg_name,
        )
        self.delimiter = getattr(
            settings,
            "DRF_NESTEDQUERYFIELDS_DELIMITER",
            self.delimiter,
        )

        try:
            request = self.context["request"]
            method = request.method
        except (AttributeError, TypeError, KeyError):
            # The serializer was not initialized with request context.
            return

        if method != "GET":
            return

        query_params = request.query_params

        includes = query_params.getlist(self.include_arg_name)
        include_field_names = {
            name for names in includes for name in names.split(self.delimiter) if name
        }

        excludes = query_params.getlist(self.exclude_arg_name)
        exclude_field_names = {
            name for names in excludes for name in names.split(self.delimiter) if name
        }

        if not include_field_names and not exclude_field_names:
            # No user fields filtering was requested, we have nothing to do here.
            return

        serializer_field_names = set(self.fields)
        nested_exclude_fields = {}
        nested_include_fields = {}
        superfields = []

        if exclude_field_names:
            for exclusion in exclude_field_names:
                if "." in exclusion:
                    splitted = re.split("\.", exclusion)
                    if splitted[0] not in nested_exclude_fields:
                        new_subfield = set()
                        nested_exclude_fields[splitted[0]] = new_subfield
                        superfields.append(splitted[0])
                    nested_exclude_fields[splitted[0]].add(splitted[1])
            for field in exclude_field_names:
                exclude_field_names.add(field)

        fields_to_drop = serializer_field_names & exclude_field_names

        if include_field_names:
            for inclusion in include_field_names:
                if "." in inclusion:
                    splitted = re.split("\.", inclusion)
                    if splitted[0] not in nested_include_fields:
                        new_subfield = set()
                        nested_include_fields[splitted[0]] = new_subfield
                        superfields.append(splitted[0])
                    nested_include_fields[splitted[0]].add(splitted[1])
            for field in nested_include_fields:
                include_field_names.add(field)

            fields_to_drop |= serializer_field_names - include_field_names

        for field in fields_to_drop:
            self.fields.pop(field)

        if not superfields:
            return

        subfield_list = []
        fields_to_drop = set()

        for field in superfields:
            deep_field = self.fields.get(field)
            if isinstance(deep_field, serializers.ModelSerializer):
                serializer_field_names = set(deep_field.fields)

                if nested_exclude_fields:
                    fields_to_drop = (
                        serializer_field_names & nested_exclude_fields[field]
                    )
                if include_field_names:
                    fields_to_drop |= (
                        serializer_field_names - nested_include_fields[field]
                    )

                for dropped_field in fields_to_drop:
                    deep_field.fields.pop(dropped_field)

                subfield_list.append(deep_field)
            fields_to_drop = set()
