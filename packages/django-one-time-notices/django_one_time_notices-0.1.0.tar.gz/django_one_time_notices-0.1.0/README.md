# django-one-time-notices

Displays a modal with notice content if a user hasn't seen it yet.

## Install
```
pip install django-one-time-notices
```

## Settings

Add to `INSTALLED_APPS`:

```
django.contrib.auth
django.contrib.admin
...
notices
```


Add to `TEMPLATES['OPTIONS']`:
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                ...
                'django.core.context_processors.request'
                ...
                'notices.context_processors.notices',
            ]
        }
    }
]
```             

## Static assets
Add `notices/css/notices.css` and `notices/js/notices.js` to your markup.

## Usage
In templates, load the tags:
```
{% load notices_tags %}
```

and add the modal:
```
{% NoticesModal %} 
```

The modal will be shown.  Once it has been dismissed it won't be shown again unless the notice version changes (see below) or the `notice_seen` cookie is deleted.

## Setting/updating the notice

### via models and django admin
Add a `Notice` instance in the django admin. 

Notices have `title`, `content`, `version` and optional `expires_at` fields.

Version can be any positive number; it defaults to incrementing the last version number.  Set the `expires_at` datetime to avoid showing this notice after the specified date, even if the user has never seen/dismissed it.

To show a new notice, add another Notice instance with an incremented version number.

### via django settings

Override the Notice model by adding to your `settings.py`:
`NOTICES_VERSION` # an integer
`NOTICES_TITLE`  # optional, default = "New!"
`NOTICES_CONTENT`  # optional, default = ""

Set `NOTICES_VERSION = 0` to clear the cookie and disable showing notices at all.
