from django.views.generic import ListView, DetailView
from .models import Discount, Category, ProductVariant
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from .models import Product, Category, Table


class DiscountList(ListView):
    model = Discount
    template_name = "discount_list.html"


class DiscountDetailView(DetailView):
    model = Discount
    template_name = "serveHub/discount_detail.html"


class CategoryList(ListView):
    model = Category
    template_name = "category_list.html"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "serveHub/category_detail.html"


def home(request):
    return render(request, "home.html")


class ProductListView(View):
    def get(self, request):
        categories = Category.objects.all()
        selected_category_id = request.GET.get('category')
        
        if selected_category_id:
            selected_category = get_object_or_404(Category, id=selected_category_id)
            products = Product.objects.filter(category=selected_category).prefetch_related('variants').order_by('name')
        else:
            selected_category = None
            products = Product.objects.prefetch_related('variants').all().order_by('category__type', 'name')
        
        return render(request, "serveHub/product_list.html", {
            'products': products,
            'categories': categories,
            'selected_category': selected_category
        })


class ProductCreateView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "serveHub/product_form.html", {"categories": categories})

    def post(self, request):
        name = request.POST.get("name")
        name_en = request.POST.get("name_en")
        category_id = request.POST.get("category")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        category = get_object_or_404(Category, id=category_id)

        try:
            product = Product.objects.create(
                name=name,
                name_en=name_en,
                category=category,
                description=description,
                image=image,
            )
            messages.success(request, f'محصول "{product.name}" با موفقیت ایجاد شد.')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f"خطا در ایجاد محصول: {str(e)}")
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
        name_en = request.POST.get("name_en")
        category_id = request.POST.get("category")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        category = get_object_or_404(Category, id=category_id)

        try:
            product.name = name
            product.name_en = name_en
            product.category = category
            product.description = description

            if image:
                product.image = image

            product.save()

            messages.success(request, f'محصول "{product.name}" با موفقیت بروزرسانی شد.')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f"خطا در بروزرسانی محصول: {str(e)}")
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
        messages.success(request, f'محصول "{product_name}" با موفقیت حذف شد.')
        return redirect('product_list')


class ProductVariantCreateView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, "serveHub/variant_form.html", {"product": product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        
        size = request.POST.get("size")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")

        try:
            variant = ProductVariant.objects.create(
                product=product,
                size=size,
                price=price,
                quantity=quantity
            )
            messages.success(request, f'نوع "{size}" با موفقیت اضافه شد.')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f"خطا در ایجاد نوع محصول: {str(e)}")
            return render(request, "serveHub/variant_form.html", {"product": product})


class ProductVariantUpdateView(View):
    def get(self, request, id):
        variant = get_object_or_404(ProductVariant, id=id)
        return render(request, "serveHub/variant_form.html", {"variant": variant})

    def post(self, request, id):
        variant = get_object_or_404(ProductVariant, id=id)
        
        variant.size = request.POST.get("size")
        variant.price = request.POST.get("price")
        variant.quantity = request.POST.get("quantity")
        variant.save()

        messages.success(request, f'نوع "{variant.size}" با موفقیت بروزرسانی شد.')
        return redirect('product_list')


class ProductVariantDeleteView(View):
    def post(self, request, id):
        variant = get_object_or_404(ProductVariant, id=id)
        variant.delete()
        messages.success(request, "نوع محصول با موفقیت حذف شد.")
        return redirect('product_list')



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
            messages.error(request, "شماره میز تکراری است.")
            return render(request, "serveHub/table_form.html")

        try:
            table = Table.objects.create(
                table_number=table_number,
                capacity=capacity,
                duration=duration,
                price=price,
            )
            messages.success(request, f'میز شماره {table.table_number} با موفقیت ایجاد شد.')
            return redirect('table_list')
        except Exception as e:
            messages.error(request, f"خطا در ایجاد میز: {str(e)}")
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
                messages.error(request, "شماره میز تکراری است.")
                return render(request, "serveHub/table_form.html", {"object": table})

        try:
            table.table_number = table_number
            table.capacity = capacity
            table.duration = duration
            table.price = price
            table.save()

            messages.success(request, f'میز شماره {table.table_number} با موفقیت بروزرسانی شد.')
            return redirect('table_list')
        except Exception as e:
            messages.error(request, f"خطا در بروزرسانی میز: {str(e)}")
            return render(request, "serveHub/table_form.html", {"object": table})