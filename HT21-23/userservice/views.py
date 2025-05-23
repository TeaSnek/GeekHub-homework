from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.shortcuts import resolve_url
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm


from products import models


class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'userservice/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login
            return redirect('products:landing')  # Redirect to main page
        return render(request, 'userservice/signup.html', {'form': form})


class LoginFormView(LoginView):
    template_name = 'userservice/login.html'
    next_page = 'products:landing'


class CartListView(LoginRequiredMixin, ListView):
    template_name = 'userservice/cart_list.html'
    context_object_name = 'cart_list'

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        self.object_list = {models.Product.objects.get(
            sears_id=key): quantity for key, quantity in cart.items()}
        context = self.get_context_data()
        return self.render_to_response(context)


@login_required
def add_to_cart(request, ):
    data = request.POST
    quantity = int(data['quantity'])
    redir = request.POST.get('reverse', 'products:product_detail')
    if quantity > 0:
        if not request.session.get('cart', {}):
            request.session['cart'] = {data['product']: quantity}
        else:
            try:
                request.session['cart'][data['product']] += quantity
                request.session.modified = True
            except KeyError:
                request.session['cart'][data['product']] = quantity
                request.session.modified = True
    try:
        return HttpResponseRedirect(reverse(redir,
                                            args=(data['product'],)))
    except NoReverseMatch:
        return HttpResponseRedirect(reverse(redir,))


@login_required
def remove_from_cart(request, ):
    data = request.POST
    quantity = int(data['quantity'])
    try:
        if not (0 < quantity <= request.session.get(
                'cart', {})[data['product']]):
            return HttpResponseRedirect(reverse('userservice:cart',))
    except KeyError:
        return HttpResponseRedirect(reverse('userservice:cart',))

    request.session['cart'][data['product']] -= quantity
    if request.session['cart'][data['product']] == 0:
        request.session['cart'].pop(data['product'], None)
    request.session.modified = True
    return HttpResponseRedirect(reverse('userservice:cart',))


@login_required
def flush_cart(request, ):
    data = request.POST
    redir = data.get('reverse', 'userservice:cart')
    if request.session.get('cart', {}):
        request.session['cart'].clear()
    request.session.modified = True
    return HttpResponseRedirect(reverse(redir,))


@login_required
def logout_view(request):
    data = request.POST
    redir = data.get('reverse', 'products:landing')
    logout(request)
    return HttpResponseRedirect(reverse(redir))
