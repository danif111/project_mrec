from django.urls import path
from mytig import views

urlpatterns = [
    path('books/', views.ListeDeLivres.as_view()),
    path('book/<int:pk>/', views.DetailLivre.as_view()),
    path('suggest/word/<search>', views.Suggestion.as_view()),
    path('search/word/<search>/', views.FindWord.as_view()),
    # path('availableproducts/', views.DispoList.as_view()),
    # path('availableproduct/<int:pk>/', views.DispoDetail.as_view()),
]
