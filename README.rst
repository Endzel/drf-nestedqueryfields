Django REST Framework Nested QueryFields 🪜
=================================

|gh|_ |codecov|_ |womm|_

.. |gh| image:: https://github.com/Endzel/drf-nestedqueryfields/actions/workflows/main.yml/badge.svg
.. _gh: https://github.com/Endzel/drf-nestedqueryfields/actions

.. |codecov| image:: https://codecov.io/gh/Endzel/drf-nestedqueryfields/graph/badge.svg?token=Y8OCVJX7MF
.. _codecov: https://codecov.io/gh/Endzel/drf-nestedqueryfields

.. |womm| image:: https://cdn.rawgit.com/nikku/works-on-my-machine/v0.2.0/badge.svg
.. _womm: https://github.com/nikku/works-on-my-machine

Allows clients to control which fields will be sent in the API response, *now in a multidimensional nest of levels!*
Fields are specified in the query and separated by points determining a given depth with no limit, e.g.

.. code-block:: 

    # You want a list of users but you're only interested in the fields "email" and "username":
    
    GET /users/?fields=email,username
    
    [
      {
        "email": "bruno@gmail.com",
        "username": "bruno"
      },
      {
        "email": "endzel@gmail.com",
        "username": "endzel"
      }
    ]

    
    # You want to see every field except "id" for the specific user endzel:
    
    GET /users/2/?fields!=id
    
    {
        "username": "endzel",
        "email": "endzel@gmail.com",
        "drinks": "tea",
        "location": {
            "id": 1,
            "country_name": "Spain",
            "city": "Málaga"
        }
    }

    
    # And, you just want to filter "username" and "city" for the "location" attribute within the user endzel:
    
    GET /users/2/?fields=username,location.city
    
    {
        "username": "endzel",
        "location": {
            "city": "Málaga"
        }
    }

**Supported Django versions**: 3.2 - 5.0+.  Check the `CI matrix <https://github.com/Endzel/drf-nestedqueryfields/blob/main/.github/workflows/main.yml/>`_ for details.

Documentation is hosted on `Read The Docs <http://drf-nestedqueryfields.readthedocs.io/>`_.

Developers, developers, developers!
-----------------------------------

Want to contribute to the project? This is how to run the test suite:

.. code-block:: bash

   # Get the repo (hopefully with a ⭐)
   git clone https://github.com/Endzel/drf-nestedqueryfields.git

   # Create and activate your virtual environment
   python -m venv .venv
   source .venv/bin/activate

   # Install the app
   pip install --editable ".[dev]"
   git checkout -b myfeature

   # Do your thing, and then fire the tests with
   python -m pytest


Many thanks to `Wim Glenn <https://github.com/wimglenn>`_, author of the original `DRF QueryFields repository <https://github.com/wimglenn/djangorestframework-queryfields>`_ from which this one was forked that inspired me to add my two cents!