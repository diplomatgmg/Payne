from django.views.generic import TemplateView

from apps.products.models import Product
from mixins.views import TitleMixin


class IndexTemplateView(TitleMixin, TemplateView):
    template_name = 'index/index.html'
    title = 'Главная'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        best_rating_products = Product.objects.order_by('-rating', 'price')[:9].select_related('brand')
        context['best_rating_product'] = best_rating_products[0]
        context['best_rating_products'] = best_rating_products[1:]

        context['best_price_products'] = Product.objects.order_by('price', '-rating')[:8].select_related('brand')
        context['best_sellers_products'] = Product.objects.order_by('-count_sales', 'price')[:4].select_related('brand')
        return context
