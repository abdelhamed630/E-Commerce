from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from .forms import CouponApplyForm
from .models import Coupon
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST)
    now = timezone.now()
    if form.is_valid():
        code=form.cleaned_data['code']
        try:
            coupon=Coupon.objects.get(code__iexact=code, vailed_from__lte=now, vailed_to__gte=now, active=True)
            request.session['coupon_id']=coupon.id
            
        except Coupon.DoesNotExist:
            request.session['coupon_id']=None
    return redirect('cart:cart_detail')

            
        
    
