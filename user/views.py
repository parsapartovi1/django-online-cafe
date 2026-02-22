from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.views import View
from .models import User , Reply
from .models import Comment, Product
from django.http import HttpResponseBadRequest
from .models import WorkingShift
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password



class UserRegisterView(View):
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        number = request.POST.get('number')
        password = request.POST.get('password')

        if User.objects.filter(number=number).exists():
            messages.error(request, 'This number is already registered.')
            return render(request, 'user/register.html')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            number=number,
            password=make_password(password)
        )

        messages.success(request, 'Registration successful. Please log in.')
        return redirect('user_login')


class UserLoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        number = request.POST.get('number')
        password = request.POST.get('password')

        try:
            user = User.objects.get(number=number)
        except User.DoesNotExist:
            messages.error(request, 'This number is not registered.')
            return render(request, 'user/login.html')

        if not check_password(password, user.password): 
            messages.error(request, 'Incorrect password.')
            return render(request, 'user/login.html')

        request.session['user_id'] = user.id
        return redirect('user_profile')

class UserProfileView(View):
    def get(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('user_login')

        user = User.objects.get(id=user_id)
        return render(request, 'user/profile.html', {'user': user})

class UserLogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('user_login')


class ChangePasswordView(View):

    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('user_login')

        return render(request, 'change_password.html')

    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('user_login')

        user = User.objects.get(id=user_id)

        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not check_password(old_password, user.password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')

        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')

        user.password = make_password(new_password1)
        user.save()

        messages.success(request, 'Password changed successfully.')
        return redirect('user_profile')

@login_required
def create_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        text = request.POST.get('text')
        com_rate = request.POST.get('com_rate')

        if not text or not com_rate:
            return HttpResponseBadRequest("Text and rating are required.")

        try:
            com_rate = float(com_rate)
            if com_rate < 1 or com_rate > 5:
                return HttpResponseBadRequest("Rating must be between 1 and 5.")
        except ValueError:
            return HttpResponseBadRequest("Invalid rating value.")


        Comment.objects.create(
            user=request.user,
            product=product,
            text=text,
            com_rate=com_rate
        )

        return redirect('product_detail', pk=product.id)


    return render(request, 'user/create_comment.html', {'product': product})




def product_comments(request):
    # Try to get product_id from GET or POST
    product_id = request.GET.get("product_id") or request.POST.get("product_id")

    # If no product_id, redirect somewhere (like home page)
    if not product_id:
        return redirect('product_list')  # or any page you want

    # Get the product
    product = get_object_or_404(Product, id=product_id)

    # Get its comments
    comments = Comment.objects.filter(product=product, is_delete=False)

    # Render a template
    return render(request, 'user/product_comments.html', {
        'product': product,
        'comments': comments
    })



class AddReply(View):
    def get(self, request, comment_id):

        if not request.user.is_authenticated:
            messages.error(request , 'please log in to add a reply.')
            return redirect('user_login')

        comment = get_object_or_404(Comment, id=comment_id)

        return render(request, 'user/add_reply.html', {'comment': comment})

    def post(self, request, comment_id):

        if not request.user.is_authenticated:
            messages.error(request, 'please log in to add a reply.')
            return redirect('user_login')

        text = request.POST.get('text')

        if text:

            comment = get_object_or_404(Comment, id=comment_id)
            reply = Reply.objects.create(
                user=request.user,
                comment=comment,
                text=text
            )
            messages.success(request, 'your reply has been added successfully.')
            return redirect('comment_detail', comment_id=comment.id)
        else:
            messages.error(request, 'please enter your reply text.')
            return redirect('add_reply', comment_id=comment_id)


def create_working_shift(request):
    if request.method == "POST":
        weekdays = request.POST.get('weekdays')
        opening_date = request.POST.get('opening_date')
        closed_date = request.POST.get('closed_date')


        if not weekdays or not opening_date or not closed_date:
            return HttpResponseBadRequest("All fields are required.")

        try:
            from datetime import datetime
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
            closed_date=closed_date_parsed
        )

        return redirect('list_working_shifts')



    return render(request, 'user/create_working_shift.html')

@login_required
def list_working_shifts(request):
    shifts = WorkingShift.objects.filter(user=request.user)
    return render(request, 'user/list_working_shifts.html', {'shifts': shifts})



