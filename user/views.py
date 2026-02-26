from datetime import datetime

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from serveHub.models import CafeWorkingHour, Product

from .models import Comment, Reply

User = get_user_model()

WEEKDAY_LABELS_FA = {
    0: "دوشنبه",
    1: "سه‌شنبه",
    2: "چهارشنبه",
    3: "پنج‌شنبه",
    4: "جمعه",
    5: "شنبه",
    6: "یکشنبه",
}


def _safe_next_url(request, value):
    if value and url_has_allowed_host_and_scheme(
        url=value,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return value
    return ""


class UserRegisterView(View):
    def get(self, request):
        return render(request, "user/register.html")

    def post(self, request):
        number = request.POST.get("number", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if not number or not email or not password:
            messages.error(request, "شماره، ایمیل و رمز عبور الزامی است.")
            return render(request, "user/register.html")

        if password != password2:
            messages.error(request, "رمز عبور و تکرار آن یکسان نیست.")
            return render(request, "user/register.html")

        if User.objects.filter(number=number).exists():
            messages.error(request, "این شماره قبلا ثبت شده است.")
            return render(request, "user/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلا ثبت شده است.")
            return render(request, "user/register.html")

        User.objects.create_user(
            number=number,
            email=email,
            password=password,
        )

        messages.success(request, "ثبت‌نام با موفقیت انجام شد. لطفا وارد شوید.")
        return redirect("user_login")


class UserLoginView(View):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        number = request.POST.get("number", "").strip()
        password = request.POST.get("password")

        if not number or not password:
            messages.error(request, "شماره و رمز عبور الزامی است.")
            return render(request, "user/login.html")

        if not User.objects.filter(number=number).exists():
            messages.error(request, "کاربری با این شماره ثبت نشده است.")
            return render(request, "user/login.html")

        user = authenticate(request, number=number, password=password)
        if user is None:
            messages.error(request, "رمز عبور اشتباه است.")
            return render(request, "user/login.html")

        login(request, user)
        return redirect("user_profile")


class UserProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("user_login")

        return render(request, "user/profile.html", {"user": request.user})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("user_login")

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()

        if len(first_name) > 24 or len(last_name) > 24:
            messages.error(request, "نام و نام خانوادگی نباید بیشتر از ۲۴ کاراکتر باشد.")
            return redirect("user_profile")

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, "پروفایل با موفقیت بروزرسانی شد.")
        return redirect("user_profile")


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("user_login")


class ChangePasswordView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("user_login")

        return render(request, "change_password.html")

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("user_login")

        user = request.user
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if not user.check_password(old_password):
            messages.error(request, "رمز فعلی اشتباه است.")
            return redirect("change_password")

        if new_password1 != new_password2:
            messages.error(request, "رمز جدید و تکرار آن یکسان نیست.")
            return redirect("change_password")

        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
        return redirect("user_profile")


@login_required
def create_comment(request, product_id):
    messages.info(
        request,
        "ثبت نظر فقط از صفحه جزئیات رزرو و پس از تایید حضور توسط مدیر امکان‌پذیر است.",
    )
    return redirect("product_detail", pk=product_id)


def product_comments(request):
    product_id = request.GET.get("product_id") or request.POST.get("product_id")
    if not product_id:
        return redirect("product_list")

    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product, is_delete=False).select_related(
        "user",
        "reply",
    )

    return render(
        request,
        "user/product_comments.html",
        {
            "product": product,
            "comments": comments,
        },
    )


@login_required
def admin_comment_list(request):
    if not request.user.is_staff:
        messages.error(request, "فقط مدیر کافه به این بخش دسترسی دارد.")
        return redirect("product_list")

    comments = Comment.objects.select_related("user", "product", "reply").order_by("-create_date")
    return render(
        request,
        "user/admin_comment_list.html",
        {"comments": comments},
    )


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    next_url = _safe_next_url(request, request.POST.get("next", ""))

    if request.user == comment.user or request.user.is_staff:
        comment.is_delete = True
        comment.save(update_fields=["is_delete", "last_update"])
        Reply.objects.filter(comment=comment).delete()
        messages.success(request, "نظر با موفقیت حذف شد.")
    else:
        messages.error(request, "اجازه حذف این نظر را ندارید.")

    if next_url:
        return redirect(next_url)
    return redirect("product_detail", pk=comment.product.id)


class AddReply(View):
    def get(self, request, comment_id):
        if not request.user.is_authenticated:
            messages.error(request, "ابتدا وارد حساب کاربری شوید.")
            return redirect("user_login")

        if not request.user.is_staff:
            messages.error(request, "فقط مدیر کافه امکان پاسخ به نظر را دارد.")
            return redirect("product_list")

        comment = get_object_or_404(Comment, id=comment_id, is_delete=False)
        if hasattr(comment, "reply"):
            messages.error(request, "برای این نظر قبلا پاسخ ثبت شده است.")
            return redirect("product_detail", pk=comment.product.id)

        next_url = _safe_next_url(request, request.GET.get("next", ""))
        return render(
            request,
            "user/add_reply.html",
            {"comment": comment, "next_url": next_url},
        )

    def post(self, request, comment_id):
        if not request.user.is_authenticated:
            messages.error(request, "ابتدا وارد حساب کاربری شوید.")
            return redirect("user_login")

        if not request.user.is_staff:
            messages.error(request, "فقط مدیر کافه امکان پاسخ به نظر را دارد.")
            return redirect("product_list")

        text = request.POST.get("text", "").strip()
        next_url = _safe_next_url(request, request.POST.get("next", ""))
        if not text:
            messages.error(request, "متن پاسخ را وارد کنید.")
            if next_url:
                return redirect(f"{request.path}?next={next_url}")
            return redirect("add_reply", comment_id=comment_id)

        comment = get_object_or_404(Comment, id=comment_id, is_delete=False)
        if hasattr(comment, "reply"):
            messages.error(request, "برای این نظر قبلا پاسخ ثبت شده است.")
            return redirect("product_detail", pk=comment.product.id)

        Reply.objects.create(
            user=request.user,
            comment=comment,
            text=text,
            is_staff=True,
        )
        comment.is_locked = True
        comment.save(update_fields=["is_locked", "last_update"])

        messages.success(request, "پاسخ با موفقیت ثبت شد.")
        if next_url:
            return redirect(next_url)
        return redirect("product_detail", pk=comment.product.id)


@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    comment = reply.comment
    next_url = _safe_next_url(request, request.POST.get("next", ""))

    if request.user == reply.user or request.user.is_staff:
        reply.delete()
        comment.is_locked = False
        comment.save(update_fields=["is_locked", "last_update"])
        messages.success(request, "پاسخ با موفقیت حذف شد.")
    else:
        messages.error(request, "اجازه حذف این پاسخ را ندارید.")

    if next_url:
        return redirect(next_url)
    return redirect("product_detail", pk=comment.product.id)


@login_required
def create_working_shift(request):
    if request.method == "POST":
        weekdays = request.POST.get("weekdays")
        opening_date = request.POST.get("opening_date")
        closed_date = request.POST.get("closed_date")

        if not weekdays or not opening_date or not closed_date:
            return HttpResponseBadRequest("All fields are required.")

        try:
            opening_date_parsed = datetime.fromisoformat(opening_date)
            closed_date_parsed = datetime.fromisoformat(closed_date)
            if closed_date_parsed <= opening_date_parsed:
                return HttpResponseBadRequest("Closed date must be after opening date.")
        except ValueError:
            return HttpResponseBadRequest("Invalid date format.")

        WorkingShift.objects.create(
            user=request.user,
            weekdays=weekdays,
            opening_date=opening_date_parsed,
            closed_date=closed_date_parsed,
        )

        return redirect("list_working_shifts")

    return render(request, "user/create_working_shift.html")


@login_required
def list_working_shifts(request):
    hours_map = {
        hour.weekday: hour
        for hour in CafeWorkingHour.objects.all().order_by("weekday")
    }
    weekly_schedule = []
    for weekday, _ in CafeWorkingHour.WEEKDAY_CHOICES:
        hour = hours_map.get(weekday)
        is_open = bool(hour and hour.is_active)
        weekly_schedule.append(
            {
                "weekday": weekday,
                "weekday_label": WEEKDAY_LABELS_FA.get(weekday, str(weekday)),
                "is_open": is_open,
                "opens_at": hour.opens_at if is_open else None,
                "closes_at": hour.closes_at if is_open else None,
            }
        )

    return render(
        request,
        "user/list_working_shifts.html",
        {"weekly_schedule": weekly_schedule},
    )


def music_page(request):
    return render(request, "music_page.html")
