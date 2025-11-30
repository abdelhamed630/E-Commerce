from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.order_id])
    return mark_safe(f'<a href="{url}" target="blank">PDF</a>')

order_pdf.short_description = 'Invoice'



def export_orders_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{opts.verbose_name_plural}.csv"'

    writer = csv.writer(response)

    # احصل على اسم الحقول
    fields = [field for field in opts.fields if not field.many_to_many and not field.one_to_many]

    # اكتب أسماء الأعمدة
    writer.writerow([field.verbose_name for field in fields])

    # اكتب البيانات
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)

            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')

            data_row.append(value)

        writer.writerow(data_row)

    return response


export_orders_to_csv.short_description = "Export Selected Orders to CSV"


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'email', 'created_at', 'paid', order_pdf)
    inlines = [OrderItemInline]
    actions = [export_orders_to_csv]
