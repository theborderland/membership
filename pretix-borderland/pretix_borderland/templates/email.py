from pretix.base.email import TemplateBasedMailRenderer

class BorderlandMailRenderer(TemplateBasedMailRenderer):
    verbose_name = 'Borderland 2023'
    identifier = 'borderland2023'
    thumbnail_filename = 'pretixbase/email/thumb.png'
    template_name = 'pretix_borderland/email/2023/plainwrapper.html'
