## Introduction

This is a project for implementing a tree menu in Django using the _“draw_menu”_ template tag.
It includes the Django application *menu*, which contains models for storing menu items; an example view for displaying a sample menu; routing for this view; templates; and most importantly, the template tag _“draw_menu”_, which takes one argument: the menu type (or label) which is defined in the menu's model.

## Description

In this test example, two types of menus are available: `main_menu` and `secondary_menu`.
The user is expected to make a request of the following type:

```
/?menu=main_menu&menu=secondary_menu&item_url=url
```

As you can see, there can be several menus on one page, but it is assumed that there is only one active element and that the URLs of the elements are unique.

## Installation

You need to download the application from the repository:
```bash
pip install git+https://github.com/ksmvrheee/uptrader-test-task.git
```

You need to register it in your project. In `settings.py`:

```
INSTALLED_APPS = [
    ...
    'menu',
]
```

Include the application's `urls.py` in the main `urls.py` of the Django project:

```
urlpatterns = [
    ...
    path('menu_app/', include('menu.urls')),
]
```

Don't forget to enable _static files serving_, as the application uses CSS to display the example view.

Also don't forget to enable `APP_DIRS` in the `TEMPLATES` in `settings.py`, as the application has it's own templates:

```
TEMPLATES = [
    {
        ...
        'APP_DIRS': True,
        ...
    }
]
```

You will need to perform migrations in the database:

```bash
python3 manage.py migrate menu
```

## Usage

Now you can populate the database, submit the request and see the test menu on the page.
Example:

```
<server_address>/<app_prefix>/example/?menu=main_menu&item_url=item_1_3_1
```

![Screenshot](https://i.ibb.co/4wfQS9K4/Screenshot-2025-07-29-190820.png)

