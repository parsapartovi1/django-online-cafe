
from django.views.generic import ListView, DetailView
from .models import Order


class OrderList(ListView):
    model = Order
    template_name = "order_list.html"


class OrderDetailView(DetailView):
    model = Order
    template_name = "order_detail.html"

# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .models import Pay, Order
from templates import payment

def create_payment(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')

        if not order_id:
            return HttpResponseBadRequest("Order is required.")

        order = get_object_or_404(Order, id=order_id)


        paid = True if status == "1" else False

        Pay.objects.create(
            user=request.user,
            order=order,
            status=paid
        )

        return redirect('list_payments')


    orders = Order.objects.all() 
    return render(request, 'payment/create_payment.html', {'orders': orders})


def list_payments(request):
    payments = Pay.objects.filter(user=request.user).order_by('-create_date')
    return render(request, 'payment/list_payment.html', {'payments': payments})

