from .models import Newspaper
from cms.models import Page
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _


class NewspaperPlugin(CMSPluginBase):
    model = Newspaper
    name = _("Newspaper")
    render_template = 'news_overview.html'

    def render(self, context, instance, placeholder):
        pages = Page.objects.public().published().filter(template=instance.news_template)
        pages = pages.order_by('publication_date')
        if instance.reverse_order:
            pages = pages.reverse()
        lang = context.get('LANGUAGE_CODE', None)
        if not lang:
            return context
        news = []
        for page in pages:
            # make sure that we only load as many items as we are supposed to.
            if instance.number and len(news) == instance.number:
                break
            # only load items that available in the right language
            if lang in page.get_languages():
                news.append(page)
        # add our news to the context so that we can render it
        context['news'] = news

        if instance.render_template:
            self.render_template = instance.render_template
        return context

plugin_pool.register_plugin(NewspaperPlugin)
