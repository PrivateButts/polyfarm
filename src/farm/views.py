from django.views.generic import ListView, DetailView

from .models import Printer


class PrinterListView(ListView):
    model = Printer
    template_name = "farm/printer_list.html"
    context_object_name = "printers"


class PrinterDetailView(DetailView):
    model = Printer
    template_name = "farm/printer_detail.html"
    context_object_name = "printer"
