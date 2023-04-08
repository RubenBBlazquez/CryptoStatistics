from django.http import JsonResponse
from CryptoStatistics.models import CryptoStatistics
from CryptoStatistics.Enums.OrderTypesEnum import OrderTypes
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render


def go_to_main_page(request):
    return render(request, template_name='index.html')


def get_symbol_from_request(request):
    get_params = request.GET
    symbol = 'BTC-USD'

    if get_params and 'symbol' in get_params.keys():
        symbol = get_params['symbol']

    return symbol


def get_bids_statistics(request):
    try:
        symbol = get_symbol_from_request(request)

        response = CryptoStatistics.get_statistics_by_order_type_and_symbol(
            str(OrderTypes.BIDS.value), symbol
        )

        return JsonResponse(data=response, status=200, safe=False)

    except ObjectDoesNotExist as err:
        return JsonResponse(data={'ko': str(err)}, status=404, safe=False)


def get_asks_statistics(request):
    try:
        symbol = get_symbol_from_request(request)

        response = CryptoStatistics.get_statistics_by_order_type_and_symbol(
            str(OrderTypes.ASKS.value), symbol
        )

        return JsonResponse(data=response, status=200, safe=False)

    except ObjectDoesNotExist as err:
        return JsonResponse(data={'ko': str(err)}, status=404, safe=False)


def get_general_statistics(request):
    response = CryptoStatistics.get_general_statistics()

    return JsonResponse(data=response, safe=False)
