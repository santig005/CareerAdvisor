from django.urls import path
from . import views

urlpatterns=[
    path('form/',views.profiling_form,name='profiling'),
    path('results/',views.results,name='results'),
]

