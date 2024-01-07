import smtplib

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from account.forms import AuthenticatedMessageForm, AnonymousMessageForm
# from .forms import Reservation
from .models import Post, DishCategory, Dish, Comment
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
        dishes = Dish.objects.all()
        context['dishes'] = dishes
        return context


class CardPage(TemplateView):
    template_name = 'coffee_card.html'

    # def cart_view(request):
    #     cart_items_count = Cart.objects.filter(
    #         user=request.user).count()  # Предполагается, что у вас есть модель Cart и связь с пользователем
    #     return render(request, 'cart.html', {'cart_items_count': cart_items_count})


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
            context['post'] = post
            context['comments'] = comments
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
