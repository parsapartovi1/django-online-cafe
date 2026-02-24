from django.urls import path
from .views import OrderList, OrderDetailView
from . import views

urlpatterns = [
    path("order/", OrderList.as_view(), name="order-list"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path(
        "reservation/<int:reservation_id>/items/add/",
        views.add_reservation_item,
        name="add_reservation_item",
    ),
    path(
        "reservation/<int:reservation_id>/cancel/",
        views.cancel_reservation,
        name="cancel_reservation",
    ),
    path(
        "reservation/<int:reservation_id>/attendance/",
        views.mark_attendance,
        name="mark_attendance",
    ),
    path(
        "reservation/<int:reservation_id>/manager-decision/",
        views.set_reservation_decision,
        name="set_reservation_decision",
    ),
    path(
        "reservation/<int:reservation_id>/review/",
        views.leave_reservation_review,
        name="leave_reservation_review",
    ),
    path("pay/create/", views.create_payment, name="create_payment"),
    path("pay/list/", views.list_payments, name="list_payments"),
]
