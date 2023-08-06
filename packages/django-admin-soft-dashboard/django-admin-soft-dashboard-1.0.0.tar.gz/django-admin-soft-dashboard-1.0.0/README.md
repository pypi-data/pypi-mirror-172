# [Django Admin Soft](https://github.com/app-generator/django-admin-soft-dashboard) 

Modern template for **Django Admin Interface** coded on top of **Soft UI Dashboard**, an open-source `Boostrap 5` design from `Creative-Tim`.

> Actively supported by [AppSeed](https://appseed.us/) via `Email` and `Discord`.

<br>

**Links & Resources**

- [Django Soft Dashboard](https://appseed.us/product/soft-ui-dashboard/django/) - free starter with the same design
- [Django Soft Dashboard](https://django-soft-ui-dashboard.appseed-srv1.com/) - LIVE Demo

<br />

![Django Admin Soft - Template project for Django provided by AppSeed.](https://user-images.githubusercontent.com/51070104/175773323-3345d618-0e78-4c85-83fc-f495dc3f0bb0.png)

<br>

## Why `Django Admin Soft`

- Modern `Bootstrap 5` Design
- `Responsive Interface`
- `Minimal Template` overriding
- `Easy integration`

<br />

## How to use it

<br />

> **Install the package** via `PIP` 

```bash
$ pip install django-admin-soft-dashboard
// OR
$ pip install git+https://github.com/app-generator/django-admin-soft-dashboard.git
```

<br />

> Add `admin_soft` application to the `INSTALLED_APPS` setting of your Django project `settings.py` file (note it should be before `django.contrib.admin`):

```python
    INSTALLED_APPS = (
        ...
        'admin_soft.apps.AdminSoftDashboardConfig',
        'django.contrib.admin',
    )
```

<br />

> **Collect static** if you are in `production environment`:

```bash
$ python manage.py collectstatic
```

<br />

> **Start the app**

```bash
$ # Set up the database
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Create the superuser
$ python manage.py createsuperuser
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
```

Access the `admin` section in the browser: `http://127.0.0.1:8000/`

<br />

## Screenshots

> **Soft UI Theme** - `Admin Section` 

![Django Admin Soft (Dark Mode) - Template project for Django provided by AppSeed.](https://user-images.githubusercontent.com/51070104/192209421-c71ebb42-7851-47eb-9942-6054e2010b82.jpg)

<br />

> **Soft UI Theme** - `SignIN Page` 

![Django Admin Soft (Login Page) - Template project for Django provided by AppSeed.](https://user-images.githubusercontent.com/51070104/192209441-2182d38f-814e-4123-ad54-7c3b580198fe.jpg) 

<br />

---
**[Django Admin Soft](https://github.com/app-generator/django-admin-soft-dashboard)** - Modern Admin Interface provided by **[AppSeed](https://appseed.us/)**
