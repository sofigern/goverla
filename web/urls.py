from django.contrib import admin
from django.urls import path

import api.views as views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', views.index),
    path('api', views.api),
    path('csv', views.post_csv),
    path('', views.goverla),
    path('goverla', views.goverla),
    path('base', views.base),
    path('lot_form/', views.lot_view, name='lot_form'),
]

