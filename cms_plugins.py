from cms.models import Page
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from .models import NewsFilter


class NewsFilterPlugin(CMSPluginBase):
    model = NewsFilter
    name = _("News Filter")
    render_template = 'news_overview.html'

    def render(self, context, instance, placeholder):
        pages = Page.objects.public().published().filter(template=instance.news_template)
        lang = context.get('LANGUAGE_CODE', None)
        if not lang:
            return context
        news = []
        for page in pages:
            # make sure that we only load as many items as we are supposed to.
            if len(news) == instance.number:
                break
            # only load items that available in the right language
            if lang in page.get_languages():
                news.append(page)
        # sort the object, showing the newest first
        news = sorted(news, key=lambda x: x.publication_date, reverse=True)
        # add our news to the context so that we can render it
        context['news'] = news
        return context

plugin_pool.register_plugin(NewsFilterPlugin)
