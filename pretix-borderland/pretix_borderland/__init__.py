from django.utils.translation import ugettext_lazy
try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

import os
from django.conf import settings

class PluginApp(PluginConfig):
    name = 'pretix_borderland'
    verbose_name = 'Pretix Borderland Customizations'

    # Inject our own translation as early as possible, before other components
    # are instantiated.
    #settings.ALL_LANGUAGES.append(('en-bl', 'English (Borderland)'))
    settings.LANGUAGES.append(('en-bl', 'English (Borderland)'))

    localepath = os.path.dirname(__file__) + '/pretix-locale'
    if os.access(localepath, os.W_OK | os.X_OK):
        settings.LOCALE_PATHS.append(localepath)

    class PretixPluginMeta:
        name = ugettext_lazy('Pretix Borderland Customizations')
        author = '@darkturo, Kris, Michi: et al'
        description = ugettext_lazy('Language, e-mail template, lottery registration etc for the Borderland')
        visible = True
        version = '1.0.0'
#        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA

default_app_config = 'pretix_borderland.PluginApp'
