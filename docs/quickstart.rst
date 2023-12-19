Quickstart
----------

Specify your base model serializer like this:

.. code-block:: python

    from rest_framework.serializers import ModelSerializer
    from drf_nestedqueryfields import NestedQueryFieldsMixin

    class MyModelSerializer(NestedQueryFieldsMixin, ModelSerializer):
        pass


Yeah, that's pretty much it.
