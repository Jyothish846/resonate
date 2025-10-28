from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox_view, name='inbox'),
    path('<int:thread_id>/', views.thread_view, name='thread'),
    path('start/<str:username>/', views.start_thread_view, name='start_thread'),
]