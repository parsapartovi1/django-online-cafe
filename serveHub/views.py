from django.views.generic import ListView, DetailView
from .models import Discount, Category
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views import View
from .models import Product, Category, Table
from django.core.paginator import Paginator


class DiscountList(ListView):
    model = Discount
    template_name = "discount_list.html"
    context_object_name = "discounted_products"


class DiscountDetailView(DetailView):
    model = Discount
    template_name = "serveHub/discount_detail.html"


class CategoryList(ListView):
    model = Category
    template_name = "serveHub/category_list.html"
    context_object_name = "categories"


# class CategoryDetailView(DetailView):
#     model = Category
#     template_name = "serveHub/category_detail.html"
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'serveHub/category_detail.html'
    context_object_name = 'category'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # دریافت محصولات مرتبط با این دسته‌بندی
        products = Product.objects.filter(category=self.object)
        
        # صفحه‌بندی محصولات
        paginator = Paginator(products, 12)  # 12 محصول در هر صفحه
        page_number = self.request.GET.get('page')
        context['products'] = paginator.get_page(page_number)
        
        # آمار اضافی (اختیاری)
        context['total_products'] = products.count()
        
        return context

def home(request):
    return render(request, "home.html")


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all().order_by("name")
        return render(request, "serveHub/product_list.html", {"products": products})


class ProductCreateView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "serveHub/product_form.html", {"categories": categories})

    def post(self, request):
        name = request.POST.get("name")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("image")

        category = get_object_or_404(Category, id=category_id)

        try:
            product = Product.objects.create(
                name=name,
                price=price,
                category=category,
                quantity=quantity,
                image=image,
            )
            messages.success(request, f'Product "{product.name}" created successfully.')
            return render(
                request,
                "serveHub/success.html",
                {"message": "Product created successfully!"},
            )
        except Exception as e:
            messages.error(request, f"Error creating product: {str(e)}")
            categories = Category.objects.all()
            return render(
                request, "serveHub/product_form.html", {"categories": categories}
            )


class ProductUpdateView(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        categories = Category.objects.all()
        return render(
            request,
            "serveHub/product_form.html",
            {"object": product, "categories": categories},
        )

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)

        name = request.POST.get("name")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("image")

        category = get_object_or_404(Category, id=category_id)

        try:
            product.name = name
            product.price = price
            product.category = category
            product.quantity = quantity

            if image:
                product.image = image

            product.save()

            messages.success(request, f'Product "{product.name}" updated successfully.')
            return render(
                request,
                "serveHub/success.html",
                {"message": "Product updated successfully!"},
            )
        except Exception as e:
            messages.error(request, f"Error updating product: {str(e)}")
            categories = Category.objects.all()
            return render(
                request,
                "serveHub/product_form.html",
                {"object": product, "categories": categories},
            )


class ProductDeleteView(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        return render(
            request, "serveHub/product_confirm_delete.html", {"object": product}
        )

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully.')
        return render(
            request,
            "serveHub/success.html",
            {"message": "Product deleted successfully!"},
        )


class TableListView(View):
    def get(self, request):
        tables = Table.objects.all().order_by("table_number")
        return render(request, "serveHub/table_list.html", {"tables": tables})


class TableCreateView(View):
    def get(self, request):
        return render(request, "serveHub/table_form.html")

    def post(self, request):
        table_number = request.POST.get("table_number")
        capacity = request.POST.get("capacity")
        duration = request.POST.get("duration")
        price = request.POST.get("price")

        if Table.objects.filter(table_number=table_number).exists():
            messages.error(request, "The table number is duplicate.")
            return render(request, "serveHub/table_form.html")

        try:
            table = Table.objects.create(
                table_number=table_number,
                capacity=capacity,
                duration=duration,
                price=price,
            )
            messages.success(
                request, f"Table #{table.table_number} created successfully."
            )
            return render(
                request,
                "serveHub/success.html",
                {"message": "Table created successfully!"},
            )
        except Exception as e:
            messages.error(request, f"Error creating table: {str(e)}")
            return render(request, "serveHub/table_form.html")


class TableUpdateView(View):
    def get(self, request, id):
        table = get_object_or_404(Table, id=id)
        return render(request, "serveHub/table_form.html", {"object": table})

    def post(self, request, id):
        table = get_object_or_404(Table, id=id)

        table_number = request.POST.get("table_number")
        capacity = request.POST.get("capacity")
        duration = request.POST.get("duration")
        price = request.POST.get("price")

        if table.table_number != int(table_number):
            if Table.objects.filter(table_number=table_number).exists():
                messages.error(request, "The table number is duplicate.")
                return render(request, "serveHub/table_form.html", {"object": table})

        try:
            table.table_number = table_number
            table.capacity = capacity
            table.duration = duration
            table.price = price
            table.save()

            messages.success(
                request, f"Table #{table.table_number} updated successfully."
            )
            return render(
                request,
                "serveHub/success.html",
                {"message": "Table updated successfully!"},
            )
        except Exception as e:
            messages.error(request, f"Error updating table: {str(e)}")
            return render(request, "serveHub/table_form.html", {"object": table})
