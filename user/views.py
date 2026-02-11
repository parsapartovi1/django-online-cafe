from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.views import View
from .models import User , Comment , Reply
from django.contrib.auth import authenticate, login, logout

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
