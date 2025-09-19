from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('hidden/', views.hidden_movies, name='movies.hidden'),
    path('petition/', views.petition, name='movies.petition'),
    path('petition/<int:petition_id>/vote/', views.vote_petition, name='movies.vote_petition'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/hide/', views.hide_movie, name='movies.hide'),
    path('<int:id>/unhide/', views.unhide_movie, name='movies.unhide'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('<int:id>/like/', views.like_movie, name='movies.like'),
]