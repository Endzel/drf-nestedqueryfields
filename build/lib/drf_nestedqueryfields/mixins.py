from django.conf import settings


class NestedQueryFieldsMixin(object):
    # If using Django filters in the API, these labels mustn't conflict with any model field names.
    include_arg_name = "fields"
    exclude_arg_name = "fields!"

    # Split field names by this string.  It doesn't necessarily have to be a single character.
    # Avoid RFC 1738 reserved characters i.e. ';', '/', '?', ':', '@', '=' and '&'
    delimiter = ","

    def __init__(self, *args, **kwargs):
        super(NestedQueryFieldsMixin, self).__init__(*args, **kwargs)
        self.include_arg_name = getattr(
            settings,
            "DRF_QUERYFIELDS_INCLUDE_ARG_NAME",
            self.include_arg_name,
        )
        self.exclude_arg_name = getattr(
            settings,
            "DRF_QUERYFIELDS_EXCLUDE_ARG_NAME",
            self.exclude_arg_name,
        )
        self.delimiter = getattr(
            settings,
            "DRF_QUERYFIELDS_DELIMITER",
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

        fields_to_drop = serializer_field_names & exclude_field_names
        if include_field_names:
            fields_to_drop |= serializer_field_names - include_field_names

        for field in fields_to_drop:
            self.fields.pop(field)
