from requests import request
from rest_framework.response import Response

from xj_payment.models import PaymentPayment


class PaymentService:
    @staticmethod
    def create(data):
        print(data)
        payment_order = PaymentPayment.objects.create(**data)
        return Response({
            'err': 0,
            'msg': '',
            'data': {
                "contact_book_id": payment_order.id,
            }})
