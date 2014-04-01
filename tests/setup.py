_setup = False

def setup():
    global _setup

    if _setup:
        return
    
    from django.conf import settings
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=(
            'configuration',
            'django.contrib.contenttypes',
            'test_app',
        ),
    )
    from django.core.management import call_command
    call_command('syncdb')
    _setup = True
