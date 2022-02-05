from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Customer E-mail feedback
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    # Create mail with recipe
    subject = 'Mój sklep - rachunek nr {}'.format(order.id)
    message = 'W załączniku przesyłamy rachunek.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
    # Create pdf file
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach pdf file
    email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
    # send email message
    email.send()
