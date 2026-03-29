# AA Permission Management

[![Version](https://img.shields.io/pypi/v/aa-permission-management?label=release)](https://pypi.org/project/aa-permission-management/)
[![License](https://img.shields.io/github/license/ppfeufer/aa-permission-management)](https://github.com/ppfeufer/aa-permission-management/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/aa-permission-management)](https://pypi.org/project/aa-permission-management/)
[![Django](https://img.shields.io/pypi/djversions/aa-permission-management?label=django)](https://pypi.org/project/aa-permission-management/)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ppfeufer/aa-permission-management/master.svg)](https://results.pre-commit.ci/latest/github/ppfeufer/aa-permission-management/master)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](http://black.readthedocs.io/en/latest/)
[![Checks](https://github.com/ppfeufer/aa-permission-management/actions/workflows/automated-checks.yml/badge.svg)](https://github.com/ppfeufer/aa-permission-management/actions/workflows/automated-checks.yml)
[![codecov](https://codecov.io/gh/ppfeufer/aa-permission-management/graph/badge.svg?token=p2qVe7q36D)](https://codecov.io/gh/ppfeufer/aa-permission-management)
[![Translation status](https://weblate.ppfeufer.de/widget/alliance-auth-apps/aa-permission-management/svg-badge.svg)](https://weblate.ppfeufer.de/engage/alliance-auth-apps/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/ppfeufer/aa-permission-management/blob/master/CODE_OF_CONDUCT.md)
[![Discord](https://img.shields.io/discord/399006117012832262?label=discord)](https://discord.gg/fjnHAmk)
[![Alliance Auth Compatibility](https://img.shields.io/badge/Alliance_Auth-v4_%7C_v5-brightgreen)](https://gitlab.com/allianceauth/allianceauth)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N8CL1BY)

Django Permission Management in the Alliance Auth Frontend

______________________________________________________________________

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Overview](#overview)
- [Installation](#installation)
  - [Bare Metal Installation](#bare-metal-installation)
    - [Step 1: Install the Module](#step-1-install-the-module)
    - [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth)
    - [Step 3: Run Static Collection, Migrations, and Restart Alliance Auth](#step-3-run-static-collection-migrations-and-restart-alliance-auth)
  - [Docker Installation](#docker-installation)
    - [Step 1: Add the App](#step-1-add-the-app)
    - [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth-1)
    - [Step 3: Build Auth and Restart Your Containers](#step-3-build-auth-and-restart-your-containers)
    - [Step 4: Finalize the Installation](#step-4-finalize-the-installation)
- [Changelog](#changelog)
- [Translation Status](#translation-status)
- [Contributing](#contributing)

<!-- mdformat-toc end -->

______________________________________________________________________

## Overview<a name="overview"></a>

This module provides a user interface for managing permissions within the Alliance
Auth application. It allows to assign and revoke permissions for groups, and states.

![AA Permission Management](https://raw.githubusercontent.com/ppfeufer/aa-permission-management/master/docs/images/presentation/aa-permission-management.jpg "AA Permission Management")

For EVE Online alliances, the number of people in a group or state can grow quite
large, which can lead to performance issues when trying to manage permissions
through the admin backend. This module provides a more efficient way to manage
permissions for large groups and states in the Alliance Auth frontend.

> [!WARNING]
>
> This module provides a user interface for managing permissions, which is an
> administrative task. \
> Please ensure to only grant access to this module to trusted users!

## Installation<a name="installation"></a>

To install the AA Permission Management module, follow these steps:

### Bare Metal Installation<a name="bare-metal-installation"></a>

#### Step 1: Install the Module<a name="step-1-install-the-module"></a>

Make sure you're in the virtual environment (venv) of your Alliance Auth
installation Then install the latest release directly from PyPi.

```shell
pip install aa-permission-management==0.0.2
```

#### Step 2: Configure Alliance Auth<a name="step-2-configure-alliance-auth"></a>

Add `aa_permission_management` to the `INSTALLED_APPS` in your `local.py` file.

```python
INSTALLED_APPS += [
    # ...
    "aa_permission_management",  # https://github.com/ppfeufer/aa-permission-management
    # ...
]
```

#### Step 3: Run Static Collection, Migrations, and Restart Alliance Auth<a name="step-3-run-static-collection-migrations-and-restart-alliance-auth"></a>

After adding the module to your configuration, run the following commands:

```shell
python manage.py collectstatic --noinput
python manage.py migrate aa_permission_management

sudo systemctl restart supervisor
```

### Docker Installation<a name="docker-installation"></a>

#### Step 1: Add the App<a name="step-1-add-the-app"></a>

Add the app to your `conf/requirements.txt`:

```
aa-permission-management==0.0.2
```

#### Step 2: Configure Alliance Auth<a name="step-2-configure-alliance-auth-1"></a>

Add `aa_permission_management` to the `INSTALLED_APPS` in your `local.py` file.

```python
INSTALLED_APPS += [
    # ...
    "aa_permission_management",  # https://github.com/ppfeufer/aa-permission-management
    # ...
]
```

#### Step 3: Build Auth and Restart Your Containers<a name="step-3-build-auth-and-restart-your-containers"></a>

After adding the module to your requirements and updating the configuration, build
your Docker images and restart your containers to apply the changes.

```shell
docker compose build --no-cache
docker compose --env-file=.env up -d
```

#### Step 4: Finalize the Installation<a name="step-4-finalize-the-installation"></a>

After the containers are up and running, run the migrations for the new module.

```shell
docker compose exec allianceauth_gunicorn bash

auth collectstatic
auth migrate
```

## Changelog<a name="changelog"></a>

See [CHANGELOG.md]

## Translation Status<a name="translation-status"></a>

[![Translation status](https://weblate.ppfeufer.de/widget/alliance-auth-apps/aa-permission-management/multi-auto.svg)](https://weblate.ppfeufer.de/engage/alliance-auth-apps/)

Do you want to help translate this app into your language or improve the existing
translation? - [Join our team of translators][weblate engage]!

## Contributing<a name="contributing"></a>

You want to contribute to this project? That's cool!

Please make sure to read the [Contribution Guidelines].\
(I promise, it's not much, just some basics)

<!-- Links -->

[changelog.md]: https://github.com/ppfeufer/aa-permission-management/blob/master/CHANGELOG.md "CHANGELOG.md"
[contribution guidelines]: https://github.com/ppfeufer/aa-permission-management/blob/master/CONTRIBUTING.md "Contribution Guidelines"
[weblate engage]: https://weblate.ppfeufer.de/engage/alliance-auth-apps/
