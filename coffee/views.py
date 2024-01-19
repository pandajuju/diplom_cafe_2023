import smtplib

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from account.forms import AuthenticatedMessageForm, AnonymousMessageForm
from .forms import ReservationForm, BillingDetailsForm
from .models import Post, DishCategory, Dish, Comment, PostCategory, Tag, Reservation, OrderDishesList, UserData, Order
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.urls import reverse_lazy, reverse


class IndexPage(TemplateView):
    template_name = 'coffee_home.html'
    form_class = ReservationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        excluded_category_name = 'Coffee'
        categories = DishCategory.objects.exclude(name=excluded_category_name)[:3]

        category_name = 'Coffee'
        dishes_coffee = Dish.objects.filter(category__name=category_name, is_visible=True)[:4]
        recent_posts = Post.objects.order_by('-date_posted')[:4]
        cart = self.request.session.get('cart', {})
        cart_items_count = sum(cart.values())

        context['recent_posts'] = recent_posts
        context['categories'] = categories
        context['dishes_coffee'] = dishes_coffee
        context['cart_items_count'] = cart_items_count
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
            return self.render_to_response(self.get_context_data(form=form))


class MenuPage(TemplateView):
    template_name = 'coffee_menu.html'
    form_class = ReservationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = DishCategory.objects.all()
        recent_posts = Post.objects.order_by('-date_posted')[:2]
        cart = self.request.session.get('cart', {})
        cart_items_count = sum(cart.values())

        context['categories'] = categories
        context['recent_posts'] = recent_posts
        context['cart_items_count'] = cart_items_count
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
            return self.render_to_response(self.get_context_data(form=form))


class ServicesPage(TemplateView):
    template_name = 'coffee_services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        recent_posts = Post.objects.order_by('-date_posted')[:4]
        cart = self.request.session.get('cart', {})
        cart_items_count = sum(cart.values())

        context['cart_items_count'] = cart_items_count
        context['recent_posts'] = recent_posts
        return context


class BlogPage(TemplateView):
    template_name = 'coffee_blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all().order_by('-date_posted')
        recent_posts = Post.objects.order_by('-date_posted')[:4]
        cart = self.request.session.get('cart', {})
        cart_items_count = sum(cart.values())

        category_id = self.request.GET.get('category')
        tag_id = self.request.GET.get('tag')

        if category_id:
            category = get_object_or_404(PostCategory, id=category_id)
            posts = posts.filter(category=category)

        if tag_id:
            tag = get_object_or_404(Tag, id=tag_id)
            posts = posts.filter(tags=tag)

        paginator = Paginator(posts, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['recent_posts'] = recent_posts
        context['page_obj'] = page_obj
        context['cart_items_count'] = cart_items_count

        return context


class AboutPage(TemplateView):
    template_name = 'coffee_about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = 'Coffee'
        recent_posts = Post.objects.order_by('-date_posted')[:2]
        dishes_coffee = Dish.objects.filter(category__name=category_name, is_visible=True)[:4]
        cart = self.request.session.get('cart', {})
        cart_items_count = sum(cart.values())

        context['recent_posts'] = recent_posts
        context['dishes_coffee'] = dishes_coffee
        context['cart_items_count'] = cart_items_count
        return context


class ContactPage(TemplateView):
    template_name = 'coffee_contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        recent_posts = Post.objects.order_by('-date_posted')[:2]
        cart_items_count = sum(cart.values())

        context['cart_items_count'] = cart_items_count
        context['recent_posts'] = recent_posts
        return context

    def post(self, request, *args, **kwargs):
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')

        if subject and message and email:
            try:
                send_mail(
                    subject,
                    message,
                    email,
                    ['u.juliana.serg@ukr.net'],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return HttpResponseRedirect(reverse_lazy('coffee:home'))
        else:
            return HttpResponse("Make sure all fields are entered and valid.")


class ShopPage(TemplateView):
    template_name = 'coffee_shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = DishCategory.objects.filter(is_visible=True).prefetch_related('dishes')
        recent_posts = Post.objects.order_by('-date_posted')[:2]
        cart = self.request.session.get('cart', {})
        cart_items_count = sum(cart.values())

        context['recent_posts'] = recent_posts
        context['categories'] = categories
        context['cart_items_count'] = cart_items_count
        return context


class CartPage(View):
    template_name = 'coffee_card.html'

    def get(self, request):
        recent_posts = Post.objects.order_by('-date_posted')[:2]
        category_name = 'Coffee'
        cart = request.session.get('cart', {})
        products_in_cart = []
        dishes_coffee = Dish.objects.filter(category__name=category_name, is_visible=True)[:4]
        total_amount = 0
        cart_items_count = 0

        for product_id, quantity in cart.items():
            product = Dish.objects.get(id=product_id)
            total_for_product = product.price * quantity
            total_amount += total_for_product
            cart_items_count += quantity
            products_in_cart.append({'product': product, 'quantity': quantity, 'total_for_product': total_for_product})

        context = {
            'dishes_coffee': dishes_coffee,
            'recent_posts': recent_posts,
            'products_in_cart': products_in_cart,
            'total_amount': total_amount,
            'cart_items_count': cart_items_count,
        }

        return render(request, self.template_name, context)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_posts = Post.objects.order_by('-date_posted')[:3]
        categories_with_counts = PostCategory.objects.annotate(num_posts=Count('posts'))
        cart = self.request.session.get('cart', {})
        cart_items_count = sum(cart.values())

        total_amount = 0
        for product_id, quantity in cart.items():
            product = Dish.objects.get(id=product_id)
            total_amount += product.price * quantity

        context['tags'] = Tag.objects.all()
        context['recent_posts'] = recent_posts
        context['categories_with_counts'] = categories_with_counts
        context['cart_items_count'] = cart_items_count
        context['total_amount'] = total_amount
        context['form'] = BillingDetailsForm()
        return context

    def post(self, request):
        form = BillingDetailsForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(order_status='Pending')

            user_data = UserData.objects.create(
                order=order,
                user=request.user if request.user.is_authenticated else None,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                street_name=form.cleaned_data['street_name'],
                house_number=form.cleaned_data['house_number'],
                phone=form.cleaned_data['phone'],
                email_address=form.cleaned_data['email_address']
            )

            recent_posts = Post.objects.order_by('-date_posted')[:2]
            total_amount = 0
            for product_id, quantity in request.session['cart'].items():
                product = Dish.objects.get(id=product_id)
                OrderDishesList.objects.create(
                    user_data=user_data,
                    order=order,
                    dish=product,
                    price=product.price,
                    quantity=quantity)
                total_amount += product.price * quantity

            del request.session['cart']

            return render(request, 'order_created.html',
                          {'order': order, 'total_amount': total_amount, 'recent_posts': recent_posts})
        else:
            context = {
                'form': form,
                'errors': form.errors
            }

        return render(request, self.template_name, context)


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
            recent_posts = Post.objects.order_by('-date_posted')[:5]
            tags = post.tags.all()
            cart = self.request.session.get('cart', {})
            cart_items_count = sum(cart.values())

            context['recent_posts'] = recent_posts
            context['post'] = post
            context['comments'] = comments
            context['categories_with_counts'] = categories_with_counts
            context['tags'] = tags
            context['cart_items_count'] = cart_items_count

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

            category_id = self.request.POST.get('category')
            tag_id = self.request.POST.get('tag')
            url = reverse('coffee:blog') + f'?category={category_id}&tag={tag_id}&id={kwargs.get("id")}'
            return redirect(url)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = comment_form
            return self.render_to_response(context)
