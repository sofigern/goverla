from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

import api.views as views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', views.index),
    path('api', views.api),
    path('csv', views.post_csv),
    path('', views.goverla),
    path('transactions/', views.transactions_api),
    path('base', views.base),
    path('lot_form/', views.lot_view, name='lot_form'),
    path('500/', TemplateView.as_view(template_name='500.html'), name='server_error'),
]
