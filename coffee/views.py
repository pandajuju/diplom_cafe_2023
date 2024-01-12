import smtplib

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from account.forms import AuthenticatedMessageForm, AnonymousMessageForm
from .forms import ReservationForm
# from .forms import Reservation
from .models import Post, DishCategory, Dish, Comment, PostCategory, Tag, Reservation
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.urls import reverse_lazy


class IndexPage(TemplateView):
    template_name = 'coffee_home.html'

    def your_view(request):
        if request.GET.get(''):
            return redirect('/')


# def reserve_table(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         last_name = request.POST['last_name']
#         date = request.POST['date']
#         time = request.POST['time']
#         phone = request.POST['phone']
#         message = request.POST['message']
#
#         reservation = Reservation.objects.create(
#             name=name,
#             last_name=last_name,
#             date=date,
#             time=time,
#             phone=phone,
#             message=message
#         )
#     return redirect('/')


class MenuPage(TemplateView):
    template_name = 'coffee_menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = DishCategory.objects.all()
        context['categories'] = categories
        return context


class ServicesPage(TemplateView):
    template_name = 'coffee_services.html'


class BlogPage(TemplateView):
    template_name = 'coffee_blog.html'

    def get_context_data(self, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return {'page_obj': page_obj}


class AboutPage(TemplateView):
    template_name = 'coffee_about.html'


class ContactPage(TemplateView):
    template_name = 'coffee_contact.html'

    def post(self, request, *args, **kwargs):
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        if subject and message and email:
            try:
                smtplib.SMTP_SSL()
                send_mail(subject, message, email, ['u.juliana.serg@ukr.net'], False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect(reverse_lazy('coffee:home'))
        else:
            return HttpResponse("Make sure all fields are entered and valid.")
        # username = request.POST.get('username') if request.user.is_authenticated else None

        # return HttpResponseRedirect('')


class ShopPage(TemplateView):
    template_name = 'coffee_shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = DishCategory.objects.filter(is_visible=True).prefetch_related('dishes')
        context['categories'] = categories
        return context


class CartPage(TemplateView):
    def get(self, request):
        cart = request.session.get('cart', {})
        products_in_cart = []
        total_amount = 0
        cart_items_count = 0

        for product_id, quantity in cart.items():
            product = Dish.objects.get(id=product_id)
            total_for_product = product.price * quantity
            total_amount += total_for_product
            cart_items_count += quantity
            products_in_cart.append({'product': product, 'quantity': quantity, 'total_for_product': total_for_product})

        return render(request, 'coffee_card.html', {'products_in_cart': products_in_cart, 'total_amount': total_amount})


class AddToCartView(TemplateView):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session['cart'] = cart

        return redirect('coffee:shop')


class RemoveFromCartView(TemplateView):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')

        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart

        return redirect('coffee:cart')


class UpdateCartView(TemplateView):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart', {})
        if product_id in cart and quantity > 0:
            cart[product_id] = quantity
            request.session['cart'] = cart

        return redirect('coffee:cart')


class CheckoutPage(TemplateView):
    template_name = 'coffee_checkout.html'


class MessageFormMixin:

    def get_message_form(self, request):
        if request.user.is_authenticated:
            return AuthenticatedMessageForm
        else:
            return AnonymousMessageForm


class BlogSinglePage(MessageFormMixin, TemplateView):
    model = Post
    template_name = 'coffee_blog_single.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            post_id = kwargs.get('id')
            post = Post.objects.get(id=post_id)
            comments = post.comments.filter(parent=None).order_by('date_posted')
            categories_with_counts = PostCategory.objects.annotate(num_posts=Count('posts'))
            recent_posts = Post.objects.order_by('-date_posted')[:3]
            tags = post.tags.all()
            print(tags)
            context['recent_posts'] = recent_posts
            context['post'] = post
            context['comments'] = comments
            context['categories_with_counts'] = categories_with_counts
            context['tags'] = tags
        except Post.DoesNotExist:
            raise Http404("Post does not exist.")

        form = self.get_message_form(self.request)
        context['form'] = form()
        return context

    def post(self, request, *args, **kwargs):

        form_class = self.get_message_form(self.request)
        parent_id = self.request.POST.get('parent_id')
        comment_form = form_class(self.request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)

            if request.user.is_authenticated:
                comment.author = request.user.username
                comment.email = request.user.email

            comment.post = Post.objects.get(id=kwargs.get('id'))

            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment

            comment.save()
            return redirect('coffee:blog_single', id=kwargs.get('id'))
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = comment_form
            return context


class Shop(TemplateView):
    def get(self, request, dish_id):
        cart = request.session.get('cart', {})
        request.session['cart'] = cart

        return redirect('coffee_card.html')


class BookTableMultiPageView(TemplateView):
    template_name = 'coffee_home.html'
    form_class = ReservationForm

    def get(self, request):
        form = self.form_class(initial=request.session.get('form_data', None))
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            request.session['form_data'] = form.cleaned_data

            reservation = Reservation(
                name=form.cleaned_data['name'],
                last_name=form.cleaned_data['last_name'],
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                phone=form.cleaned_data['phone'],
                message=form.cleaned_data['message'],
                is_processed=False)
            reservation.save()

            return redirect('menu')
        return render(request, self.template_name, {'form': form})