# django-data-history

A Django application that allows you to store detailed data in the change log and display the detailed information in object's history view.

## Install

```
pip install django-data-history
```

## Usage

```

## add app: django_middleware_global_request
## add app: django_middleware_request_id
## add app: django_static_jquery_ui
## add app: django_data_history
## put django_data_history before django.contrib.admin

INSTALLED_APPS = [
    ...
    "django_middleware_global_request",
    "django_middleware_request_id",
    "django_static_jquery_ui",
    'django_data_history',
    ...
    'django.contrib.admin',
    ...
]

## add middleware: django_middleware_global_request.middleware.GlobalRequestMiddleware
## add middleware: django_middleware_request_id.middlewares.DjangoMiddlewareRequestId
MIDDLEWARE = [
    ...
    "django_middleware_global_request.middleware.GlobalRequestMiddleware",
    "django_middleware_request_id.middlewares.DjangoMiddlewareRequestId",
    ...
]

# default to False, so you must set it to True to enable all models injection.
SAVE_DATA_HISTORIES_FOR_ALL = True 

# if SAVE_DATA_HISTORIES_FOR_ALL==False, then only these models will be injected.
# default to empty.
SAVE_DATA_HISTORIES_FOR = [
    "your_app1.model_name1"
]

# if SAVE_DATA_HISTORIES_FOR_ALL==True, these models will NOT be injected.
# default to:
# [
#    "sessions.session",
#    "contenttypes.contenttype",
#    "admin.logentry",
#    "auth.permission",
# ]
DO_NOT_SAVE_DATA_HISTORIES_FOR = [
    "your_app2.model_name2",
]

```

## Instance's history view

![django-date-history-view-preview](https://github.com/zencore-dobetter/pypi-images/raw/main/django-data-history/django-data-history.png)

## Releases

### v0.1.0

- First release.

### v0.1.1

- Fix ugettext_lazy problem.

### v0.1.2

- Add save_data_histories_for_fk_instance to fix inline edit history missing problem.

### v0.1.3

- Fix problems that field name has "+" in fields_map.

### v0.1.5

- Using django_middleware_request_id instead of implement request_id inside the app.
