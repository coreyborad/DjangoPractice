from datetime import datetime
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from order.models import Order, Order_item


def index(request):
    return render(request, 'index.html')


def sample(request):
    cohort = Order._getCohortInfo()
    return render(
        request,
        'sample.html',
        {
            'shipinfo': Order._getShippingInfo(),
            'date_list': cohort['date_list'],
            'cohort_result': cohort['fortable'],
            'rank': Order_item._getRank(),
        }
    )


def upload(request):
    if request.method == 'POST':
        try:
            order_csv = request.FILES['order_csv']
            order_item_csv = request.FILES['order_item_csv']

            # Check file name
            if not order_csv.name.endswith('.csv'):
                return HttpResponseRedirect(reverse('index'))
            if not order_item_csv.name.endswith('.csv'):
                return HttpResponseRedirect(reverse('index'))

            # Check file size
            if order_csv.multiple_chunks():
                return HttpResponseRedirect(reverse('index'))
            if order_item_csv.multiple_chunks():
                return HttpResponseRedirect(reverse('index'))

            # Start create
            order_csv = order_csv.read().decode('utf-8').splitlines()
            Order._create(order_csv)
            order_item_csv = order_item_csv.read().decode('utf-8').splitlines()
            Order_item._create(order_item_csv)

            return JsonResponse({
                'status': True
            })
        except Exception as e:
            return JsonResponse({
                'status': False,
                'msg': e
            })
    else:
        return HttpResponseRedirect(reverse('sample'))
