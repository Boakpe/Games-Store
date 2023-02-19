from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from accounts.forms import CustomUserCreationForm

from games.models import PurchaseItem


""" class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html' """
    
@login_required
def perfilView(request):
    games = PurchaseItem.objects.filter(purchase__user=request.user).exclude(refunded=True)
    return render(request, 'accounts/account.html', {'user': request.user, 'games': games})

def registerUserView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_date['username']
            password = form.cleaned_date['password1']
            user = authenticate(username = username, password = password)
            #login(request, user)
            return redirect('')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})