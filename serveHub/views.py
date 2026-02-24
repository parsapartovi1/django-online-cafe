from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView

from payment.models import Reservation
from user.models import Comment

from .models import CafeWorkingHour, Category, Discount, Product, Table

WEEKDAY_LABELS_FA = {
    0: "دوشنبه",
    1: "سه‌شنبه",
    2: "چهارشنبه",
    3: "پنج‌شنبه",
    4: "جمعه",
    5: "شنبه",
    6: "یکشنبه",
}


class DiscountList(ListView):
    model = Product
    template_name = "serveHub/discount_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(
            size__discount__isnull=False,
            size__discount__duration__gt=timezone.now(),
        ).select_related("size", "size__discount")


class DiscountDetailView(DetailView):
    model = Discount
    template_name = "serveHub/discount_detail.html"


class CategoryList(ListView):
    model = Category
    template_name = "serveHub/category_list.html"
    context_object_name = "category_list"
    queryset = Category.objects.all().order_by("type")


def home(request):
    return render(request, "home.html")


class ProductListView(View):
    def get(self, request):
        categories = Category.objects.all()
        selected_category_id = request.GET.get("category")

        if selected_category_id:
            selected_category = get_object_or_404(Category, id=selected_category_id)
            products = Product.objects.filter(category=selected_category)
        else:
            selected_category = None
            products = Product.objects.all().order_by("category__type", "name")

        return render(
            request,
            "serveHub/product_list.html",
            {
                "products": products,
                "categories": categories,
                "selected_category": selected_category,
            },
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "serveHub/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = (
            Comment.objects.filter(product=self.object, is_delete=False)
            .select_related("user", "reply")
            .order_by("-create_date")
        )
        return context


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    request.session["cart"] = cart

    messages.success(request, f"{product.name} به سبد خرید اضافه شد.")
    return redirect("order-list")


class TableReservationView(View):
    def get(self, request):
        tables = Table.objects.filter(is_available=True)
        selected_type = request.GET.get("type")

        if selected_type:
            tables = tables.filter(table_type=selected_type)

        table_types = Table.TABLE_TYPES
        working_hours = {}
        weekly_working_hours = []
        hours_map = {
            hour.weekday: hour
            for hour in CafeWorkingHour.objects.all().order_by("weekday")
        }

        for weekday, _ in CafeWorkingHour.WEEKDAY_CHOICES:
            hour = hours_map.get(weekday)
            is_open = bool(hour and hour.is_active)

            if is_open:
                opens_at = hour.opens_at.strftime("%H:%M")
                closes_at = hour.closes_at.strftime("%H:%M")
                working_hours[weekday] = {
                    "opens_at": opens_at,
                    "closes_at": closes_at,
                }
            else:
                opens_at = None
                closes_at = None

            weekly_working_hours.append(
                {
                    "weekday": weekday,
                    "weekday_label": WEEKDAY_LABELS_FA.get(weekday, str(weekday)),
                    "is_open": is_open,
                    "opens_at": opens_at,
                    "closes_at": closes_at,
                }
            )

        return render(
            request,
            "serveHub/table_reservation.html",
            {
                "tables": tables,
                "table_types": table_types,
                "selected_type": selected_type,
                "working_hours": working_hours,
                "weekly_working_hours": weekly_working_hours,
            },
        )


class ReserveTableView(LoginRequiredMixin, View):
    def post(self, request, table_id):
        table = get_object_or_404(Table, id=table_id, is_available=True)
        people_count_raw = request.POST.get("people_count")
        reservation_datetime_raw = request.POST.get("reservation_datetime")
        reservation_date_raw = request.POST.get("reservation_date")
        reservation_time_raw = request.POST.get("reservation_time")

        if not reservation_datetime_raw and reservation_date_raw and reservation_time_raw:
            reservation_datetime_raw = f"{reservation_date_raw}T{reservation_time_raw}"

        if not people_count_raw or not reservation_datetime_raw:
            messages.error(request, "تعداد نفرات و تاریخ/ساعت رزرو الزامی است.")
            return redirect("table_reservation")

        try:
            people_count = int(people_count_raw)
        except ValueError:
            messages.error(request, "تعداد نفرات نامعتبر است.")
            return redirect("table_reservation")

        if people_count < 1:
            messages.error(request, "حداقل یک نفر باید انتخاب شود.")
            return redirect("table_reservation")

        if people_count > table.capacity:
            messages.error(request, f"ظرفیت میز حداکثر {table.capacity} نفر است.")
            return redirect("table_reservation")

        try:
            start_time = datetime.fromisoformat(reservation_datetime_raw)
        except ValueError:
            messages.error(request, "فرمت تاریخ/ساعت رزرو صحیح نیست.")
            return redirect("table_reservation")

        if timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time, timezone.get_current_timezone())

        now = timezone.now()
        if start_time <= now:
            messages.error(request, "زمان رزرو باید در آینده باشد.")
            return redirect("table_reservation")

        working_hour = CafeWorkingHour.objects.filter(
            weekday=start_time.weekday(),
            is_active=True,
        ).first()
        if not working_hour:
            messages.error(request, "در این روز کافه تعطیل است.")
            return redirect("table_reservation")

        tz = timezone.get_current_timezone()
        open_time = timezone.make_aware(
            datetime.combine(start_time.date(), working_hour.opens_at),
            tz,
        )
        close_time = timezone.make_aware(
            datetime.combine(start_time.date(), working_hour.closes_at),
            tz,
        )
        end_time = start_time + timedelta(minutes=table.duration)

        if start_time < open_time or end_time > close_time:
            messages.error(
                request,
                "زمان انتخابی خارج از ساعات کاری کافه برای این روز است.",
            )
            return redirect("table_reservation")

        offset_minutes = int((start_time - open_time).total_seconds() // 60)
        if offset_minutes % table.duration != 0:
            messages.error(
                request,
                f"زمان رزرو باید در اسلات‌های {table.duration} دقیقه‌ای باشد.",
            )
            return redirect("table_reservation")

        has_overlap = Reservation.objects.filter(
            table=table,
            status=Reservation.STATUS_RESERVED,
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).exists()
        if has_overlap:
            messages.error(request, "این میز در بازه زمانی انتخابی قبلا رزرو شده است.")
            return redirect("table_reservation")

        reservation = Reservation.objects.create(
            user=request.user,
            table=table,
            start_time=start_time,
            end_time=end_time,
            people_count=people_count,
            table_unit_price=table.price_per_person,
        )
        messages.success(request, "رزرو میز با موفقیت ثبت شد.")
        return redirect("order-detail", pk=reservation.pk)
