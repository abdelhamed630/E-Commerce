from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from io import BytesIO
from xhtml2pdf import pisa
from .models import Order
from django.conf import settings

@shared_task
def payment_completed(order_id):
    try:
        order = Order.objects.get(id=order_id)

        # توليد HTML للـ PDF
        html_content = render_to_string('order/order_pdf.html', {'order': order})
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

        if pisa_status.err:
            print(f"PDF generation error for order {order.id}")
            return False

        pdf_file.seek(0)

        # تحضير الإيميل
        email_subject = f'Invoice for Order #{order.id}'
        email_body = 'Thank you for your purchase. Please find your invoice attached.'
        email = EmailMessage(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
        )

        # إضافة PDF كمرفق
        email.attach(f'Invoice_Order_{order.id}.pdf', pdf_file.read(), 'application/pdf')
        email.send()
        return True

    except Exception as e:
        print(f"Error in payment_completed task: {e}")
        return False
