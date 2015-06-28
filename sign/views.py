from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.views.generic.edit import FormView, View
from sign.forms import LoginForm, SignupForm


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'sign/login.html'
    success_url = 'home/'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['signup'] = SignupForm
        context['login'] = LoginForm
        return context

    def get_success_url(self):
        return self.request.GET.get('next', '/')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                context = self.get_context_data(form=form)
                context['errors'] = 'This user is Inactive'
                return self.render_to_response(context)
        else:
            context = self.get_context_data(form=form)
            context['errors'] = 'LOGIN FAILED !!!'
            return self.render_to_response(context)


class LogoutView(View):
    success_url = 'home/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.success_url)
    
    
class SignupView(LoginView):
    form_class = SignupForm

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        context['errors'] = []
        if User.objects.filter(username=form.cleaned_data['s_username']).exists():
            context['errors'].append('A User with this username exists !!!')
        elif User.objects.filter(email=form.cleaned_data['s_username']).exists():
            context['errors'].append('A User with this email exists !!!')
        else:
            user = User.objects.create_user(form.cleaned_data['s_username'], form.cleaned_data['s_mail'], form.cleaned_data['s_password'])
            user.save()
            user = authenticate(username=form.cleaned_data['s_username'], password=form.cleaned_data['s_password'])
            if user:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                context = self.get_context_data(form=form)
                context['errors'] = 'REGISTRATION FAILED !!!'
                return self.render_to_response(context)

        return self.render_to_response(context)




