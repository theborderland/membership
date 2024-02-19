from pretix.base.email import TemplateBasedMailRenderer

class BorderlandMailRendererClassic(TemplateBasedMailRenderer):
    verbose_name = 'Borderland Classic'
    identifier = 'borderland2023'
    thumbnail_filename = 'pretixbase/email/thumb.png'
    template_name = 'pretix_borderland/email/2023/plainwrapper.html'

class BorderlandMailRenderer2024(TemplateBasedMailRenderer):
    verbose_name = 'Borderland 2024 Edition'
    identifier = 'borderland2024'
    thumbnail_filename = 'pretixbase/email/thumb.png'
    template_name = 'pretix_borderland/email/2024/plainwrapper.html'

