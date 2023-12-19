from setuptools import setup


classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Intended Audience :: Developers",
    "Framework :: Django",
]

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="drf-nestedqueryfields",
    version="1.0.0",
    description="Serialize API fields on demand to various levels of depth",
    long_description=long_description,
    packages=["drf_nestedqueryfields"],
    author="Ángel Jiménez",
    author_email="angeljimenezgong@gmail.com",
    license="MIT",
    url="https://github.com/Endzel/drf-nestedqueryfields",
    classifiers=classifiers,
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pytest-django",
            "coveralls",
            "django",
            "djangorestframework",
            "mock_django",
            "setuptools",
            "wheel",
            "pytz",
        ]
    },
)
