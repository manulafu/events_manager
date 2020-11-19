from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'events'

urlpatterns = [
	path('', views.index, name='index'),

	# Events urls
	path('events/', views.EventList.as_view(), name='event_list'),
	path('events/<int:pk>/', views.event_detail, name='event_detail'),
	path('events/<int:pk>/attendees/', views.attendees_list, name='attendees_list'),
	path('events/create/', views.CreateEvent.as_view(), name='create_event'),
	path('events/<int:pk>/delete/', views.DeleteEvent.as_view(), name='delete_event'),

	# Accounts urls
	path('accounts/login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
	path('accounts/logout/', LogoutView.as_view(), name='logout'),
	path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
	path('accounts/<int:pk>/delete/', views.DeleteUser.as_view(), name='delete_user'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)