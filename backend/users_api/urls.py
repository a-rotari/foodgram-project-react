from django.urls import path

from . import views

urlpatterns = [
    path('set-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions'),
    path('<int:pk>/subscribe/', views.CreateDestroySubscriptionView.as_view(),
         name='create-destroy-subscription'),
    path('<int:pk>/', views.UserProfileView.as_view(), name='user-profile'),
    path('', views.UserListCreate.as_view(), name='user-list-create'),
]
