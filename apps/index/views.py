from django.views.generic import TemplateView

from apps.products.models import Product
from mixins.views import TitleMixin


class IndexTemplateView(TitleMixin, TemplateView):
    template_name = 'index/index.html'
    title = 'Главная'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['best_rating_product'] = Product.objects.order_by('-rating').first()
        return context
