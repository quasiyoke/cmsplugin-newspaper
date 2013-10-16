from cms.models import CMSPlugin, Page
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Newspaper(CMSPlugin):
    """Saves the settings for the News."""

    template_choices = dict(Page.template_choices)

    number = models.IntegerField(_('number'), default=5, help_text=_('The number of articles that should be displayed. Left blank to omit limitation.'), blank=True)
    news_template = models.CharField(_('news template'), max_length=100, choices=Page.template_choices, help_text=_('News\' template.'))
    render_template = models.CharField(_('render template'), blank=True, max_length=100, choices=Page.template_choices, help_text=_('The template used to render the content.'))

    def __unicode__(self):
        return u'%s \xd7 %s' % (self.template_choices.get(self.news_template, self.news_template), self.number or u'\u221e', )
