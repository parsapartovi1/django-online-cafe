from django.views.generic import ListView, DetailView
from .models import Discount, Category
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from .models import Product, Category, Table
from user.models import Comment
class DiscountList(ListView):
    model = Discount
    template_name = "discount_list.html"


class DiscountDetailView(DetailView):
    model = Discount
    template_name = "serveHub/discount_detail.html"


class CategoryList(ListView):
    model = Category
    template_name = "serveHub/category_list.html"
    context_object_name = "category_list"
    queryset = Category.objects.all().order_by('type')




def home(request):
    return render(request, "home.html")


class ProductListView(View):
    def get(self, request):
        categories = Category.objects.all()
        selected_category_id = request.GET.get('category')

        if selected_category_id:
            selected_category = get_object_or_404(Category, id=selected_category_id)
            products = Product.objects.filter(category=selected_category)
        else:
            selected_category = None
            products = Product.objects.all().order_by('category__type', 'name')

        return render(request, "serveHub/product_list.html", {
            'products': products,
            'categories': categories,
            'selected_category': selected_category
        })


class ProductDetailView(DetailView):
    model = Product
    template_name = "serveHub/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            product=self.object,
            is_delete=False
        ).order_by('-create_date')
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
        selected_type = request.GET.get('type')

        if selected_type:
            tables = tables.filter(table_type=selected_type)

        table_types = Table.TABLE_TYPES

        return render(request, 'serveHub/table_reservation.html', {
            'tables': tables,
            'table_types': table_types,
            'selected_type': selected_type
        })


class ReserveTableView(View):
    def post(self, request, table_id):
        table = get_object_or_404(Table, id=table_id, is_available=True)
        people_count = request.POST.get('people_count')
        reservation_datetime = request.POST.get('reservation_datetime')

        if not people_count or not reservation_datetime:
            messages.error(request, 'لطفاً تمام موارد را پر کنید.')
            return redirect('table_reservation')

        try:
            people_count = int(people_count)
            if people_count > table.capacity:
                messages.error(request, f'ظرفیت میز حداکثر {table.capacity} نفر است.')
                return redirect('table_reservation')

            total_price = table.total_price(people_count)

            messages.success(request,
                f'میز {table.get_table_type_display()} با موفقیت برای {people_count} نفر رزرو شد. '
                f'مبلغ قابل پرداخت: {total_price:,} تومان')

        except Exception as e:
            messages.error(request, f'خطا در رزرو: {str(e)}')

        return redirect('table_reservation')


from django.shortcuts import redirect


def reserve_table(request, table_id):
    if request.method == "POST":
        # منطق ساخت رزرو اینجا

        # مثلا:
        # Reservation.objects.create(...)

        return redirect('order_list')  # 👈 این مهمه

    return redirect('table_reservation')

