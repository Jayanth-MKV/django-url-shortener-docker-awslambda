from django.urls import path
from .views import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:key>' , views.getURL),
    path('create/' , views.createLink,name='create_view'),
    path('random-link/', views.random_link, name='random_link'),
    path('search/', views.search_links, name='search_links'),
    path('update/<str:key>/', views.update_link, name='update_link'),
    path('delete/<str:key>/', views.delete_link, name='delete_link'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
