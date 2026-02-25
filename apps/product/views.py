from django.views.generic import TemplateView
from apps.product.models import Category, Product


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(
            is_active=True, parent__isnull=True)[:6]
        context['products'] = Product.objects.filter(
            is_available=True, category__is_active=True)[:8]
        return context 
       
        