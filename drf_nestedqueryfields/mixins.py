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
            # Serializer was not initialized with request context
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
            # No user fields filtering was requested
            return

        self._apply_field_filtering(include_field_names, exclude_field_names)

    def _apply_field_filtering(self, include_field_names, exclude_field_names):
        """
        Apply field filtering to this serializer and all nested serializers.
        """
        # Parse field specifications into a tree structure
        include_tree = self._parse_field_tree(include_field_names)
        exclude_tree = self._parse_field_tree(exclude_field_names)

        # Apply filtering recursively
        self._filter_fields_recursive(self, include_tree, exclude_tree)

    def _parse_field_tree(self, field_names):
        """
        Parse field names like 'province.region.name' into a nested tree structure.

        Example:
        ['name', 'province.region.name', 'province.code'] becomes:
        {
            'name': True,
            'province': {
                'region': {
                    'name': True
                },
                'code': True
            }
        }
        """
        tree = {}

        for field_name in field_names:
            # Skip empty field names
            if not field_name.strip():
                continue

            parts = [part.strip() for part in field_name.split(".") if part.strip()]

            # Skip if no valid parts after cleaning
            if not parts:
                continue

            current = tree

            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    # Last part, mark as included
                    current[part] = True
                else:
                    # Intermediate part, create nested dict if needed
                    if part not in current:
                        current[part] = {}
                    elif current[part] is True:
                        # Convert from leaf to branch
                        current[part] = {}
                    current = current[part]

        return tree

    def _filter_fields_recursive(self, serializer, include_tree, exclude_tree):
        """
        Recursively filter fields in the serializer based on include/exclude trees.
        """
        if not hasattr(serializer, "fields"):
            return

        serializer_field_names = set(serializer.fields.keys())
        fields_to_remove = set()

        if include_tree:
            included_fields = set(include_tree.keys())
            fields_to_remove |= serializer_field_names - included_fields
        if exclude_tree:
            # Exclude wins when a field is in both include and exclude.
            for field_name, value in exclude_tree.items():
                if value is True and field_name in serializer_field_names:
                    fields_to_remove.add(field_name)

        # Remove fields from current level
        for field_name in fields_to_remove:
            if field_name in serializer.fields:
                serializer.fields.pop(field_name)

        # Process nested serializers
        for field_name, field_obj in list(serializer.fields.items()):
            if isinstance(field_obj, serializers.ModelSerializer):
                # Get nested include/exclude trees for this field
                nested_include = (
                    include_tree.get(field_name, {}) if include_tree else {}
                )
                nested_exclude = (
                    exclude_tree.get(field_name, {}) if exclude_tree else {}
                )

                # Process nested serializers if there are nested specifications
                if nested_include or nested_exclude:
                    # Convert True values to empty dict (means include the field but no nested filtering)
                    if nested_include is True:
                        nested_include = {}
                    if nested_exclude is True:
                        nested_exclude = {}

                    # Recursively filter the nested serializer
                    self._filter_fields_recursive(
                        field_obj, nested_include, nested_exclude
                    )
