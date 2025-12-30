from django.urls import path
from .views import NotificationListView

urlpatterns = [
        path('', include('notifications.urls')),
        path('notifications/', NotificationListView.as_view()),
]

