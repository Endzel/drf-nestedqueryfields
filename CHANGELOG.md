# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-05-20

### Fixed
- Declare `Django>=4.2` and `djangorestframework>=3.14` as runtime
  dependencies. Previously `pip install drf-nestedqueryfields` left these
  to the caller, which meant a fresh install failed to import.

### Added
- Expose `__version__` from `drf_nestedqueryfields` for tooling that
  introspects installed package versions.
- PyPI sidebar links to Documentation, Source, Issues, and Changelog.
- CI now tests against Django 4.2 LTS, 5.2 LTS, and the latest release,
  plus declared-floor combinations (Django 4.2 with DRF 3.14 and 3.15) to
  verify the lower bounds work end-to-end rather than just being claimed.

### Security
- Pinned third-party GitHub Actions (`actions/checkout`,
  `actions/setup-python`, `actions/upload-artifact`,
  `actions/download-artifact`, `codecov/codecov-action`,
  `pypa/gh-action-pypi-publish`) to specific commit SHAs across all
  workflows, mitigating supply-chain risk from action tag re-pointing.

## [1.0.0] - 2026-05-20

First release under the new maintainer (forked from
[djangorestframework-queryfields](https://github.com/wimglenn/djangorestframework-queryfields)).

### Added
- Nested field filtering at arbitrary depth using dot notation, e.g.
  `?fields=province.region.name` or `?fields!=province.region.id`.
- Tests covering depth 3-5, malformed specifications, and large numbers of
  non-existent deep paths.
- Documentation page describing the deep-nesting behaviour
  (`docs/deepnesting.rst`).

### Changed
- Recursive tree-based implementation of include/exclude filtering,
  replacing the previous single-level handler.
- `setup.py` metadata: explicit Python 3.11-3.14 and Django 4.2-6.0
  classifiers, `python_requires=">=3.11"`, RST `long_description` content
  type for correct PyPI rendering.

### Fixed
- When a field name appears in both `fields=` and `fields!=`, exclude now
  wins. The intermediate refactor had regressed this behaviour for
  overlapping include/exclude specifications.
