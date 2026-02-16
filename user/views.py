from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.views import View
from .models import User , Reply
from django.contrib.auth import authenticate, login, logout
from .models import Comment, Product
from django.http import HttpResponseBadRequest
from .models import WorkingShift
from django.contrib.auth.decorators import login_required
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

        try:

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                number=number,
                password=password
            )
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('user_login')

        except Exception as e:
            messages.error(request, f'Error during registration: {str(e)}')
            return render(request, 'user/register.html')


class UserLoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        number = request.POST.get('number')
        password = request.POST.get('password')


        user = authenticate(request, username=number, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}')
            return redirect('add_reply', comment_id=1)
        else:
            messages.error(request, 'Please check your number and password and try again.')
            return render(request, 'user/login.html')


class UserProfileView(View):
    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('user_login')

        return render(request, 'user/profile.html', {'user': request.user})


class UserLogoutView(View):
    def get(self, request):

        logout(request)

        return redirect('user_login')


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

        return redirect('product_detail', product_id=product.id)


    return render(request, 'user/create_comment.html', {'product': product})


def product_comments(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product, is_delete=False)
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
    return render(request, 'user/working_shift_list.html', {'shifts': shifts})


