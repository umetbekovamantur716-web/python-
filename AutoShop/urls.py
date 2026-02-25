from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),


    path('admin/', admin.site.urls),

    path('', include('apps.product.urls')),
    path('about/', include('apps.about.urls')),
    path('blog/', include('apps.blog.urls')),
    path('cart/', include('apps.cart.urls')),
    path('contact/', include('apps.contact.urls')),
    path('partners/', include('apps.partners.urls')),
    path('users/', include('apps.users.urls')),
]
