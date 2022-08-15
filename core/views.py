from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import redirect

from .forms import GenerateRandomUserForm
from .tasks import create_random_user_accounts, num_sum
    
def index(request):
    users = User.objects.all()
    return render(request, "user_list.html", context={"users":users})

class GenerateRndomuserView(FormView):
    template_name = 'generate_random_user.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        users = User.objects.all()
        total = form.cleaned_data.get('total')
        res = num_sum.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect("user_list")

def random(request):
    return render(request,'chat/basic_count.html',context={'text':"hello world"})

def user_list(request):
    return render(request, 'chat/user_list.html')
