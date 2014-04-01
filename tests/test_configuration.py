from tests.setup import setup
setup()
from django.test import TestCase
from django.contrib import admin
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from configuration.models import Configuration
from test_app.models import (
    AbstractConfiguration,
    EmptyConfiguration,
    SubChildConfiguration,
    AdminStringConfiguration,
    AdminModelConfiguration,
    CustomAdmin,
)
from configuration.admin import ConfigurationAdmin, ConfigurationParentAdmin
from configuration.templatetags.configuration import get_configuration


class ConfigurationTestCase(TestCase):
    def test_get_admin_class(self):
        c = Configuration()
        self.assertEqual(c.admin_class,
                         'configuration.admin.ConfigurationAdmin')
        self.assertIs(c.get_admin_class(), c.admin_class)

    def test_get_description(self):
        c = Configuration()
        self.assertEqual(c.description, 'Configuration')
        self.assertIs(c.get_description(), c.description)

    def test_repr(self):
        c = AbstractConfiguration()
        self.assertEqual(str(c), "Test test")

    def test_unique(self):
        EmptyConfiguration.objects.create()
        with self.assertRaises(IntegrityError):
            EmptyConfiguration.objects.create()


class ConfigurationManagerTestCase(TestCase):
    def test_child_get_args(self):
        with self.assertRaises(AssertionError):
            EmptyConfiguration.objects.get(1)

        with self.assertRaises(AssertionError):
            EmptyConfiguration.objects.get(pk=1)

    def test_child_get_exists(self):
        c = EmptyConfiguration.objects.create()
        self.assertEqual(c.pk, EmptyConfiguration.objects.get().pk)

    def test_child_get_new(self):
        self.assertIs(EmptyConfiguration.objects.get().pk, None)

    def test_base_get(self):
        with self.assertRaises(ObjectDoesNotExist):
            Configuration.objects.get()

        c = EmptyConfiguration.objects.create()
        Configuration.objects.get()
        Configuration.objects.get(pk=c.pk)


class ConfigurationAdminTestCase(TestCase):
    def test_permissions(self):
        ca = ConfigurationAdmin(EmptyConfiguration, admin.site)
        self.assertEqual(ca.has_add_permission(None), False)
        self.assertEqual(ca.has_delete_permission(None), False)


class ConfigurationParentAdminTestCase(TestCase):
    def test_permissions(self):
        cpa = ConfigurationParentAdmin(Configuration, admin.site)
        self.assertEqual(cpa.has_add_permission(None), False)
        self.assertEqual(cpa.has_delete_permission(None), False)

    def test_child_models(self):
        cpa = ConfigurationParentAdmin(Configuration, admin.site)
        self.assertEqual(
            cpa.get_child_models(),
            ((SubChildConfiguration, ConfigurationAdmin),
             (EmptyConfiguration, ConfigurationAdmin),
             (AdminStringConfiguration, CustomAdmin),
             (AdminModelConfiguration, CustomAdmin))
        )


class TemplateTagsTestCase(TestCase):
    def test_bad_strings(self):
        with self.assertRaisesRegexp(ValueError, "^app is not a model$"):
            get_configuration("app")

        with self.assertRaisesRegexp(ValueError,
                                     "^Could not find model app.model$"):
            get_configuration("app.model")

        with self.assertRaisesRegexp(ValueError,
                                     "^contenttypes.ContentType "
                                     "is not a Configuration$"):
            get_configuration("contenttypes.ContentType")

        with self.assertRaisesRegexp(ValueError,
                                     "^Could not find model "
                                     "test_app.AbstractConfiguration$"):
            get_configuration("test_app.AbstractConfiguration")

    def test_get(self):
        c = get_configuration("test_app.EmptyConfiguration")
        self.assertIs(type(c), EmptyConfiguration)
