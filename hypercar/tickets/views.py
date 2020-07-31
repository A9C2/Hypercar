from collections import deque, namedtuple

from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .utils import Queues

QUEUES = Queues()


class WelcomeView(View):
    def __init__(self):
        self.template_name = "tickets/welcome.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


class MenuView(View):
    def __init__(self):
        self.template_name = "tickets/menu.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


class NewTicket(View):
    def __init__(self):
        self.template_name = "tickets/new_ticket.html"

    def get(self, request, **kwargs):
        service_type = kwargs["service_type"]

        service_queue_info = QUEUES.get_by_name(service_type)
        if service_queue_info is None:
            raise Http404

        service_time = service_queue_info.time
        assert service_time > 0, "Time of doing the service must be a positive number"
        estimated_time = QUEUES.get_estimated_time(service_time)
        assert estimated_time >= 0

        ticket_number = QUEUES.last_ticket_number + 1
        QUEUES.last_ticket_number += 1

        service_queue = service_queue_info.queue
        service_queue.append(ticket_number)

        context = {"estimated_time": estimated_time, "ticket_number": ticket_number}
        return render(request, template_name=self.template_name, context=context)


class ProcessingInfo(View):
    def __init__(self):
        self.template_name = "tickets/tickets_in_queue.html"

    def get(self, request):
        context = QUEUES.get_queues_length()
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        QUEUES.set_next_ticket()
        return redirect("http://127.0.0.1:8000/processing")


class NextTicketInfo(View):
    def __init__(self):
        self.template_name = "tickets/next.html"

    def get(self, request):
        context = {"next": QUEUES.next_ticket}
        return render(request, template_name=self.template_name, context=context)
