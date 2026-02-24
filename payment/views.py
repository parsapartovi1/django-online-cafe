from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from serveHub.models import Product
from user.models import Comment

from .models import Pay, Reservation, ReservationItem


def _reservation_queryset_for_user(user):
    qs = Reservation.objects.select_related("table", "user").prefetch_related(
        "items",
        "items__product",
        "comments",
        "comments__reply",
    )
    if user.is_staff:
        return qs
    return qs.filter(user=user)


def _review_blockers_for_reservation(reservation, now=None):
    now = now or timezone.now()
    blockers = []

    if reservation.status != Reservation.STATUS_RESERVED:
        blockers.append("این رزرو فعال نیست و امکان ثبت نظر ندارد.")

    if now < reservation.start_time:
        start_local = timezone.localtime(reservation.start_time)
        blockers.append(
            f"هنوز به زمان رزرو نرسیده‌اید. زمان رزرو: {start_local.strftime('%Y-%m-%d %H:%M')}"
        )

    if reservation.attendance_status != Reservation.ATTENDANCE_PRESENT:
        blockers.append("حضور شما هنوز توسط مدیر به حالت «حاضر» ثبت نشده است.")

    if not reservation.items.exists():
        blockers.append("برای این رزرو هیچ خوراکی ثبت نشده است.")

    return blockers


class OrderList(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "payment/order_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return _reservation_queryset_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = self.request.user.is_staff
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = "payment/order_detail.html"
    context_object_name = "reservation"

    def get_queryset(self):
        return _reservation_queryset_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = self.object
        now = timezone.now()

        context["is_manager"] = self.request.user.is_staff
        context["products"] = Product.objects.select_related("category").order_by(
            "category__type",
            "name",
        )
        context["can_cancel_as_user"] = (
            reservation.user_id == self.request.user.id
            and reservation.can_user_cancel()
        )
        context["can_cancel_as_manager"] = (
            self.request.user.is_staff and reservation.can_manager_cancel()
        )
        context["can_mark_attendance"] = self.request.user.is_staff and reservation.can_mark_attendance()
        context["can_manage_decision"] = self.request.user.is_staff and reservation.can_manager_decide()
        context["attendance_wait_message"] = ""
        if self.request.user.is_staff and reservation.status == Reservation.STATUS_RESERVED and now < reservation.start_time:
            context["attendance_wait_message"] = "ثبت حضور از زمان شروع رزرو فعال می‌شود."
        user_review_exists = Comment.objects.filter(
            user=self.request.user,
            reservation=reservation,
            is_delete=False,
        ).exists()
        review_blockers = []
        if reservation.user_id == self.request.user.id and not user_review_exists:
            review_blockers = _review_blockers_for_reservation(reservation, now)
        context["review_blockers"] = review_blockers
        context["can_leave_review"] = (
            reservation.user_id == self.request.user.id
            and not user_review_exists
            and not review_blockers
        )
        context["existing_review"] = (
            Comment.objects.filter(
                user=reservation.user,
                reservation=reservation,
                is_delete=False,
            )
            .select_related("reply")
            .first()
        )
        return context


def _get_reservation_or_404_for_request(request, reservation_id):
    reservation_qs = _reservation_queryset_for_user(request.user)
    return get_object_or_404(reservation_qs, id=reservation_id)


@login_required
@require_POST
def add_reservation_item(request, reservation_id):
    reservation = _get_reservation_or_404_for_request(request, reservation_id)

    if reservation.user_id != request.user.id:
        messages.error(request, "فقط صاحب رزرو می‌تواند خوراکی اضافه کند.")
        return redirect("order-detail", pk=reservation.id)

    if reservation.status != Reservation.STATUS_RESERVED:
        messages.error(request, "برای رزرو لغو شده امکان افزودن خوراکی وجود ندارد.")
        return redirect("order-detail", pk=reservation.id)

    if timezone.now() >= reservation.start_time:
        messages.error(request, "پس از شروع زمان رزرو امکان افزودن خوراکی وجود ندارد.")
        return redirect("order-detail", pk=reservation.id)

    product_id = request.POST.get("product_id")
    quantity_raw = request.POST.get("quantity", "1")

    if not product_id:
        return HttpResponseBadRequest("Product is required.")

    try:
        quantity = int(quantity_raw)
    except ValueError:
        messages.error(request, "تعداد نامعتبر است.")
        return redirect("order-detail", pk=reservation.id)

    if quantity < 1:
        messages.error(request, "تعداد باید حداقل ۱ باشد.")
        return redirect("order-detail", pk=reservation.id)

    product = get_object_or_404(Product, id=product_id)
    unit_price = product.get_price_for_size(1)
    if unit_price <= 0:
        messages.error(request, "امکان تعیین قیمت برای این خوراکی وجود ندارد.")
        return redirect("order-detail", pk=reservation.id)

    item, created = ReservationItem.objects.get_or_create(
        reservation=reservation,
        product=product,
        defaults={"quantity": quantity, "unit_price": unit_price},
    )
    if not created:
        item.quantity += quantity
        item.unit_price = unit_price
        item.save(update_fields=["quantity", "unit_price", "update_date"])

    messages.success(request, "خوراکی با موفقیت به رزرو اضافه شد.")
    return redirect("order-detail", pk=reservation.id)


@login_required
@require_POST
def cancel_reservation(request, reservation_id):
    reservation = _get_reservation_or_404_for_request(request, reservation_id)
    now = timezone.now()

    if request.user.is_staff:
        if not reservation.can_manager_cancel(now):
            messages.error(
                request,
                "مدیر فقط وقتی بیش از یک ساعت تا شروع رزرو باقی مانده باشد امکان لغو دارد.",
            )
            return redirect("order-detail", pk=reservation.id)
        reservation.status = Reservation.STATUS_CANCELLED_BY_MANAGER
    else:
        if reservation.user_id != request.user.id:
            messages.error(request, "امکان لغو این رزرو برای شما وجود ندارد.")
            return redirect("order-detail", pk=reservation.id)
        if not reservation.can_user_cancel(now):
            messages.error(
                request,
                "پس از شروع زمان رزرو امکان لغو برای مشتری وجود ندارد.",
            )
            return redirect("order-detail", pk=reservation.id)
        reservation.status = Reservation.STATUS_CANCELLED_BY_USER

    reservation.cancelled_by = request.user
    reservation.cancelled_at = now
    reservation.save(update_fields=["status", "cancelled_by", "cancelled_at", "update_date"])

    messages.success(request, "رزرو با موفقیت لغو شد.")
    return redirect("order-detail", pk=reservation.id)


@login_required
@require_POST
def mark_attendance(request, reservation_id):
    if not request.user.is_staff:
        messages.error(request, "فقط مدیر کافه می‌تواند حضور را ثبت کند.")
        return redirect("order-list")

    reservation = get_object_or_404(Reservation, id=reservation_id)
    if not reservation.can_mark_attendance():
        messages.error(
            request,
            f"ثبت حضور فقط بعد از زمان {reservation.start_time.strftime('%Y-%m-%d %H:%M')} مجاز است.",
        )
        return redirect("order-detail", pk=reservation.id)

    attendance_status = request.POST.get("attendance_status")
    if attendance_status not in {
        Reservation.ATTENDANCE_PRESENT,
        Reservation.ATTENDANCE_ABSENT,
    }:
        messages.error(request, "وضعیت حضور نامعتبر است.")
        return redirect("order-detail", pk=reservation.id)

    reservation.attendance_status = attendance_status
    reservation.attendance_marked_by = request.user
    reservation.attendance_marked_at = timezone.now()
    reservation.save(
        update_fields=[
            "attendance_status",
            "attendance_marked_by",
            "attendance_marked_at",
            "update_date",
        ]
    )

    messages.success(request, "وضعیت حضور با موفقیت ثبت شد.")
    return redirect("order-detail", pk=reservation.id)


@login_required
@require_POST
def set_reservation_decision(request, reservation_id):
    if not request.user.is_staff:
        messages.error(request, "فقط مدیر کافه می‌تواند وضعیت رزرو را تایید یا رد کند.")
        return redirect("order-list")

    reservation = get_object_or_404(Reservation, id=reservation_id)
    if not reservation.can_manager_decide():
        messages.error(request, "این رزرو در وضعیت قابل تصمیم‌گیری نیست.")
        return redirect("order-detail", pk=reservation.id)

    manager_decision = request.POST.get("manager_decision")
    if manager_decision not in {
        Reservation.DECISION_APPROVED,
        Reservation.DECISION_REJECTED,
    }:
        messages.error(request, "وضعیت تصمیم‌گیری نامعتبر است.")
        return redirect("order-detail", pk=reservation.id)

    reservation.manager_decision = manager_decision
    reservation.manager_decided_by = request.user
    reservation.manager_decided_at = timezone.now()
    reservation.save(
        update_fields=[
            "manager_decision",
            "manager_decided_by",
            "manager_decided_at",
            "update_date",
        ]
    )

    if manager_decision == Reservation.DECISION_APPROVED:
        messages.success(request, "رزرو با موفقیت تایید شد.")
    else:
        messages.success(request, "رزرو با موفقیت رد شد.")
    return redirect("order-detail", pk=reservation.id)


@login_required
@require_POST
def leave_reservation_review(request, reservation_id):
    reservation = _get_reservation_or_404_for_request(request, reservation_id)
    if reservation.user_id != request.user.id:
        messages.error(request, "فقط صاحب رزرو می‌تواند نظر ثبت کند.")
        return redirect("order-detail", pk=reservation.id)

    if Comment.objects.filter(
        user=request.user,
        reservation=reservation,
        is_delete=False,
    ).exists():
        messages.error(request, "برای این رزرو قبلا نظر ثبت شده است.")
        return redirect("order-detail", pk=reservation.id)

    review_blockers = _review_blockers_for_reservation(reservation)
    if review_blockers:
        messages.error(request, review_blockers[0])
        return redirect("order-detail", pk=reservation.id)

    text = request.POST.get("text", "").strip()
    com_rate_raw = request.POST.get("com_rate", "").strip()
    if not text or not com_rate_raw:
        messages.error(request, "متن نظر و امتیاز الزامی است.")
        return redirect("order-detail", pk=reservation.id)

    try:
        com_rate = float(com_rate_raw)
    except ValueError:
        messages.error(request, "امتیاز نامعتبر است.")
        return redirect("order-detail", pk=reservation.id)

    if com_rate < 1 or com_rate > 5:
        messages.error(request, "امتیاز باید بین ۱ تا ۵ باشد.")
        return redirect("order-detail", pk=reservation.id)

    products = Product.objects.filter(
        reservation_items__reservation=reservation
    ).distinct()
    if not products.exists():
        messages.error(request, "برای ثبت نظر باید حداقل یک خوراکی در رزرو وجود داشته باشد.")
        return redirect("order-detail", pk=reservation.id)

    for product in products:
        Comment.objects.create(
            user=request.user,
            product=product,
            reservation=reservation,
            text=text,
            com_rate=com_rate,
        )

    messages.success(request, "نظر شما برای این رزرو ثبت شد.")
    return redirect("order-detail", pk=reservation.id)


@login_required
def create_payment(request):
    messages.info(request, "در این نسخه عملیات واقعی پرداخت انجام نمی‌شود.")
    return redirect("order-list")


@login_required
def list_payments(request):
    payments = Pay.objects.filter(user=request.user).order_by("-create_date")
    return render(request, "payment/list_payment.html", {"payments": payments})
