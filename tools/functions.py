from typing import List

from quotes.appconstants import SERVICE_TYPES


def get_show_perms(service_type):
    if service_type == SERVICE_TYPES[0][0]:
        check_origin = True
        check_freight = True
        check_destination = True
    elif service_type == SERVICE_TYPES[1][0]:
        check_origin = True
        check_freight = True
        check_destination = False
    elif service_type == SERVICE_TYPES[2][0]:
        check_origin = False
        check_freight = True
        check_destination = True
    elif service_type == SERVICE_TYPES[3][0]:
        check_origin = False
        check_freight = True
        check_destination = False

    return {
        'check_origin': check_origin,
        'check_freight': check_freight,
        'check_destination': check_destination
    }


def get_sale_price(services: List):
    total_total_sale = 0
    sum_buy_fields = 0
    for service in services:
        q = None
        s = None
        b = None
        try:
            q = int(service.quantity)
            s = int(service.sale_price)
            b = int(service.buy_price)
        except TypeError:
            continue

        vat_mult = 1.17 if service.vat else 1
        total_total_sale += q * s * vat_mult
        sum_buy_fields += q * b * vat_mult
    return sum_buy_fields, total_total_sale

