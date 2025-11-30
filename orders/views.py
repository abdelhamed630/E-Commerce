from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from xhtml2pdf import pisa

from .tasks import payment_completed
from .models import Order, OrderItem
from .forms import OrderForm, OrderPaymentForm
from cart.cart import Cart
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


# PDF للـ Admin
@login_required
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    html = render_to_string('order/order_pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.order_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response

# إنشاء الطلب
@login_required
def order_create(request):
    cart = Cart(request)
    success = False
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            
            for item in cart:
                # إذا item['product'] هو object من Product
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],  # <-- تم التصحيح هنا
                    price=item['price'],
                    quantity=item['quantity']
                )

            # مسح الكارت
            cart.clear()

            # إرسال إيميل تأكيد
            subject = 'Order Confirmation'
            message = f"Your order ID: {order.order_id} has been created successfully.\n\nOrder details:\n"
            for item in order.items.all():
                message += f"Product: {item.product.name} - {item.quantity} x ${item.price}\n"  # <-- هنا أيضاً تم التعديل

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.email])
            success = True

            return redirect('orders:pay_order', order_id=order.order_id)
    else:
        form = OrderForm()
    return render(request, 'order/created.html', {'cart': cart, 'form': form, 'success': success})


# الدفع
@login_required
def order_pay_by_vodafone(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    if request.method == 'POST':
        form = OrderPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.paid = True
            payment.save()

            # تحديث حالة الطلب
            order.paid = True
            order.save()

            # استدعاء Celery Task بعد الدفع
            payment_completed.delay(order.id)

            return redirect('orders:payment_success', order_id=order.order_id)
    else:
        form = OrderPaymentForm()
    
    return render(request, 'order/pay_form.html', {'order': order, 'form': form})


# صفحة نجاح الدفع
@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'order/payment_success.html', {'order': order})
