from setuptools import setup


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Framework :: Django",
    "Framework :: Django :: 4.2",
    "Framework :: Django :: 5.0",
    "Framework :: Django :: 5.1",
    "Framework :: Django :: 6.0",
]

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="drf-nestedqueryfields",
    version="1.0.0",
    description="Serialize API fields on demand to various levels of depth",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=["drf_nestedqueryfields"],
    author="Ángel Jiménez",
    author_email="angeljimenezgong@gmail.com",
    license="MIT",
    url="https://github.com/Endzel/drf-nestedqueryfields",
    python_requires=">=3.11",
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
