from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Sale, SaleDetail

class SaleDetailInline(admin.TabularInline):
    model = SaleDetail
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date_issued', 'total_amount', 'is_paid')
    list_filter = ('is_paid', 'date_issued')
    inlines = [SaleDetailInline]