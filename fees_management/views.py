
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from student.models import *
from student.models import Fees
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator

def login(request):
    context = dict()
    if request.user.is_authenticated: 
        return HttpResponseRedirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if request.GET.get('next', None):
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect('dashboard')
            else:
                context["error"] = "Enter Valid Credentials"
                return render(request, 'login.html', context)
        else:
            return render(request, 'login.html', context)
        return render(request, 'login.html')


@method_decorator(login_required, name='dispatch')
class Dashboard(View):

    def get(self, request, the_id=None):
        context = dict()
        context['course'] = Course.objects.all()
        context['branch'] = Branch.objects.all()
        context['fees'] = Fees.objects.all()

        if the_id:
            context['heading'] = Student.objects.filter(branch=the_id)[0]
            context['students'] = Student.objects.filter(branch=the_id)
            return render(request, 'dashboard.html', context)
        else:
            context['students'] = Student.objects.all()
            
            return render(request, 'dashboard.html', context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

