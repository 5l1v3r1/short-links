from django.urls import path

from .views import (
    LinkCreateView,
    LinkRedirectView,
    LinkListView,
    LinkDetailView,
    LinkDeleteView,
    ajax_visits_by_link
)


app_name = 'main'

urlpatterns = [
    path('', LinkCreateView.as_view(), name='index'),
    path('links/', LinkListView.as_view(), name='link-list'),
    path('detail/<int:pk>/', LinkDetailView.as_view(), name='link-detail'),
    path('delete/<int:pk>/', LinkDeleteView.as_view(), name='link-delete'),
    path('ajax/<int:pk>/', ajax_visits_by_link, name='ajax-visit-list'),
    path('<short_link>/', LinkRedirectView.as_view(), name='redirect'),
]
