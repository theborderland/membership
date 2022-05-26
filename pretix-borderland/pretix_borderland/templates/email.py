from pretix.base.email import TemplateBasedMailRenderer

class BorderlandMailRenderer(TemplateBasedMailRenderer):
    verbose_name = 'Borderland 2022'
    identifier = 'borderland2022'
    thumbnail_filename = 'pretixbase/email/thumb.png'
    template_name = 'pretix_borderland/email/2022/plainwrapper.html'