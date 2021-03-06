from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect

# Create your views here.
from products.models import Product
from .models import Order

@login_required
def order_checkout_view(request):
    qs = Product.objects.filter(featured=True)
    if not qs.exists():
        return redirect("/")

    product = qs.first()
    user = request.user
    order_id = request.session.get("order_id")
    order_obj = None

    new_creation = False

    try:
        order_obj = Order.objects.get(id=order_id)
    except:
        order_id = None

    if order_id == None:
        new_creation = True
        order_obj = Order.objects.create(product=product, user=user)
    if order_obj != None and new_creation == False:
        if order_obj.product.id != product.id:
            order_obj = Order.objects.create(product=product, user=user)
    request.session['order_id'] = order_obj.id
    return render(request, 'forms.html', {})