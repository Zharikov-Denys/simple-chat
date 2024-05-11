from wagtail.contrib.modeladmin.options import modeladmin_register

from .threads import ThreadsAdminGroup


modeladmin_register(ThreadsAdminGroup)
