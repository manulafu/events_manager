from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .forms import CreateUserForm
from .models import Event


def index(request):
	return render(request, 'index.html')


# Events Views
class EventList(ListView):
	paginate_by = 5
	model = Event
	template_name = 'events/event_list.html'
	context_object_name = 'events'
	queryset = Event.objects.all()[:20]


def event_detail(request, pk):
	event = get_object_or_404(Event, pk=pk)

	context = {
		'event': event
	}
	if request.method == 'POST':
		user = request.user
		event.attendees.add(user)
		event.save()
		return redirect('events:attendees_list', pk=pk)
	return render(request, 'events/event_detail.html', context)

def attendees_list(request, pk):
	event = get_object_or_404(Event, pk=pk)
	context = {
		'event': event
	}
	if request.method == 'POST':
		user = request.user
		if user in event.attendees.all():
			event.attendees.remove(user)
			event.save()
		else:
			event.attendees.add(user)
			event.save()
		return render(request, 'events/event_attendees.html', context)
	return render(request, 'events/event_attendees.html', context)

class CreateEvent(CreateView):
	model = Event
	fields = ['title', 'description', 'image',
	          'date', 'location', 'allowed_attendees',
	          'waitlist', 'startTime', 'endTime']
	template_name = 'events/create_event.html'

class DeleteEvent(SuccessMessageMixin, DeleteView):
	model = Event
	success_url = reverse_lazy('events:event_list')
	success_message = 'Delete event completed successfully'


# Accounts Views
class SignUpView(CreateView):
	form_class = CreateUserForm
	template_name = 'accounts/signup.html'
	success_url = reverse_lazy('events:login')

class DeleteUser(SuccessMessageMixin, DeleteView):
	model = get_user_model()
	success_url = reverse_lazy('events:index')
	template_name = 'accounts/user_confirm_delete.html'
	success_message = 'User account delete completed successfully!'
