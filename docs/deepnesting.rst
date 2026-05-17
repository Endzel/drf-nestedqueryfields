Deep Nesting Guide
==================

This guide demonstrates the deep nesting capabilities of
``drf-nestedqueryfields``. There is no fixed limit on nesting depth — the
filter is applied recursively to every nested serializer.

Examples by Depth Level
-----------------------

Level 1: Basic Filtering
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Include only specific fields
   GET /cities/?fields=name,code

   # Exclude specific fields
   GET /cities/?fields!=id,created_at

Level 2: One Level Deep
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Include nested fields
   GET /cities/?fields=name,province.name,province.code

   # Exclude nested fields
   GET /cities/?fields!=id,province.id

Level 3: Two Levels Deep
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Include deeply nested fields
   GET /cities/?fields=province.region.name,province.region.code

   # Mixed depth includes
   GET /cities/?fields=name,province.name,province.region.country.name

Level 4: Three Levels Deep
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Very deep nesting
   GET /cities/?fields=province.region.country.name,province.region.country.code

   # Exclude at deep levels
   GET /cities/?fields!=province.region.country.id

Level 5: Four Levels Deep
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Full depth across the test model
   GET /cities/?fields=province.region.country.continent.name

   # Combining include with exclude
   GET /cities/?fields=name,province.region.country.continent.name&fields!=province.id

When ``fields`` and ``fields!`` both reference the same name, exclude wins.

Beyond: Unknown or Non-existent Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Paths that don't resolve to a real field — at any depth — are silently
ignored. This keeps clients safe to request optional or speculative paths
without server errors:

.. code-block:: bash

   GET /cities/?fields=name,fake.level2.level3.level4.level5
   GET /cities/?fields=name,path1.l2.l3,path2.l2.l3.l4.l5.l6.l7

Error Handling
--------------

The following malformed inputs are tolerated and produce no errors:

.. code-block:: bash

   GET /cities/?fields=name,nonexistent.field
   GET /cities/?fields=name,....                  # Stray dots
   GET /cities/?fields=name,,province..region     # Empty parts

What gets ignored:

- Non-existent field names at any level
- Empty field specifications
- Malformed dot notation
- Fields that don't exist on nested serializers

Implementation Details
----------------------

Tree-Based Parsing
~~~~~~~~~~~~~~~~~~

Field specifications like ``province.region.country.name`` are parsed into
a nested tree:

.. code-block:: python

   {
       'province': {
           'region': {
               'country': {
                   'name': True
               }
           }
       }
   }

Recursive Processing
~~~~~~~~~~~~~~~~~~~~

- Each serializer level is processed independently
- Nested serializers are filtered recursively
- Non-existent paths are safely ignored
- Work scales with the actual depth of the serializer tree, not the depth
  of the request specification

Test Coverage
-------------

The deep-nesting behaviour is exercised by:

- ``tests/test_deep_nesting.py`` — depth 3-5 includes/excludes, mixed-depth
  operations, edge cases (empty specs, trailing dots), combined
  include/exclude.
- ``tests/test_extreme_depth.py`` — very deep bogus paths, malformed
  specifications, large numbers of bogus fields.
- ``tests/test_userfields_with_nested_modelserializers.py`` — original
  single-level suite plus added second-level cases.

Running the Tests
-----------------

.. code-block:: bash

   # Whole suite
   pytest

   # Just the deep-nesting suites
   pytest tests/test_deep_nesting.py tests/test_extreme_depth.py
