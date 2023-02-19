from django.db.models import Q
from django.views.generic import CreateView, DetailView
from django.views.generic import ListView

from mixins.views import TitleMixin
from ..products.models import Product


class ShopView(TitleMixin, ListView):
    model = Product
    template_name = 'shop/shop.html'
    title = 'Магазин'
    paginate_by = 8
    paginate_orphans = 4
    ordering = '-rating'
    search = ''

    def get(self, *args, **kwargs):
        self.ordering = self.request.GET.get('ordering', self.ordering)
        self.search = self.request.GET.get('search', '')
        return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['ordering'] = self.ordering
        context['search'] = self.search

        return context

    def get_queryset(self):
        query = ' '.join(self.request.GET.get('search', '').lower().split())
        object_list = self.model.search_products(query=query, ordering=self.ordering)
        return object_list


class ShopProductView(DetailView):
    model = Product
    template_name = 'shop/product_details.html'
