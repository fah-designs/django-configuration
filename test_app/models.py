from configuration.models import Configuration
from configuration.admin import ConfigurationAdmin


class AbstractConfiguration(Configuration):
    class Meta(object):
        abstract = True
        verbose_name = "test test"


class SubChildConfiguration(AbstractConfiguration):
    pass


class EmptyConfiguration(Configuration):
    pass


class CustomAdmin(ConfigurationAdmin):
    pass


class AdminStringConfiguration(Configuration):
    admin_class = "test_app.models.CustomAdmin"


class AdminModelConfiguration(Configuration):
    admin_class = CustomAdmin
