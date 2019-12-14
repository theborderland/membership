from pretix.base.email import TemplateBasedMailRenderer

class BorderlandMailRenderer(TemplateBasedMailRenderer):
    verbose_name = 'Borderland 2020'
    identifier = 'borderland2020'
    thumbnail_filename = 'pretixbase/email/thumb.png'
    template_name = 'pretix_borderland/email/2020/plainwrapper.html'
