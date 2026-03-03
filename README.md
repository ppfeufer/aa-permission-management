# AA Permission Management

Django Permission Management in the Alliance Auth Frontend

______________________________________________________________________

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Overview](#overview)
- [Installation](#installation)
  - [Bare Metal Installation](#bare-metal-installation)
    - [Step 1: Install the Module](#step-1-install-the-module)
    - [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth)
    - [Step 3: Restart Alliance Auth](#step-3-restart-alliance-auth)
  - [Docker Installation](#docker-installation)
    - [Step 1: Add the App](#step-1-add-the-app)
    - [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth-1)
    - [Step 3: Build Auth and Restart Your Containers](#step-3-build-auth-and-restart-your-containers)

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

## Installation<a name="installation"></a>

To install the AA Permission Management module, follow these steps:

### Bare Metal Installation<a name="bare-metal-installation"></a>

#### Step 1: Install the Module<a name="step-1-install-the-module"></a>

Make sure you're in the virtual environment (venv) of your Alliance Auth
installation Then install the latest release directly from PyPi.

```shell
pip install aa-permission-management==0.0.1a1
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

#### Step 3: Restart Alliance Auth<a name="step-3-restart-alliance-auth"></a>

After installing the module and updating the configuration, restart your Alliance
Auth application to apply the changes.

```shell
sudo systemctl restart supervisor
```

### Docker Installation<a name="docker-installation"></a>

#### Step 1: Add the App<a name="step-1-add-the-app"></a>

Add the app to your `conf/requirements.txt`:

```
aa-permission-management==0.0.1a1
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
