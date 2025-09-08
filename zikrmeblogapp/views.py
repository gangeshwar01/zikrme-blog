from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from .models import Category, HeroImage, Post, Destination, PageHeroImage, HomeMiniVideo
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category")

    posts = Post.objects.filter(is_published=True)
    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(categories__name__icontains=query)
        ).distinct()

    categories = Category.objects.all()

    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(categories=selected_category)

    featured_posts = posts.filter(is_featured=True)[:12]
    article_posts = posts.filter(is_article=True)[:12]

    hero_images = HeroImage.objects.filter(is_active=True)
    home_mini_video = HomeMiniVideo.objects.filter(is_active=True).first()

    context = {
        "hero_images": hero_images,
        "categories": categories,
        "selected_category": selected_category,
        "posts_sample": posts[:15],
        "featured_posts": featured_posts,
        "article_posts": article_posts,
        "query": query,
        "home_mini_video": home_mini_video,
    }
    return render(request, "home.html", context)


def posts_list(request):
    query = request.GET.get("q", "").strip()
    posts = Post.objects.filter(is_published=True)
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(description__icontains=query))
    paginator = Paginator(posts, 15)
    page = request.GET.get("page")
    paginated = paginator.get_page(page)
    return render(request, "posts_list.html", {"page_obj": paginated, "query": query})


def posts_by_category(request, slug: str):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(is_published=True, categories=category)
    paginator = Paginator(posts, 15)
    page = request.GET.get("page")
    paginated = paginator.get_page(page)
    return render(
        request,
        "posts_list.html",
        {"page_obj": paginated, "category": category},
    )


def featured_list(request):
    posts = Post.objects.filter(is_published=True, is_featured=True)
    paginator = Paginator(posts, 15)
    page = request.GET.get("page")
    paginated = paginator.get_page(page)
    return render(request, "posts_list.html", {"page_obj": paginated, "list_title": "Featured Posts"})


def articles_list(request):
    posts = Post.objects.filter(is_published=True, is_article=True)
    paginator = Paginator(posts, 15)
    page = request.GET.get("page")
    paginated = paginator.get_page(page)
    return render(request, "posts_list.html", {"page_obj": paginated, "list_title": "Latest Articles"})


def about(request):
    hero_image = PageHeroImage.objects.filter(page='about', is_active=True).first()
    return render(request, "about.html", {"hero_image": hero_image})


def contact(request):
    hero_image = PageHeroImage.objects.filter(page='contact', is_active=True).first()
    success = False
    error_message = None
    form = ContactForm(request.POST or None)
    
    # Debug info
    print(f"Request method: {request.method}")
    print(f"Form is valid: {form.is_valid()}")
    if request.method == "POST":
        print(f"POST data: {request.POST}")
        print(f"Form errors: {form.errors}")
    
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        subject = f"New contact message from {data['name']}"
        body = f"From: {data['name']} <{data['email']}>\n\n{data['message']}"
        try:
            from django.core.mail import EmailMessage
            email = EmailMessage(
                subject,
                body,
                data['email'],  # use sender's email as FROM
                ["01personal002@gmail.com"],
                headers={"Reply-To": data['email']},
            )
            email.send()
            success = True
            form = ContactForm()
        except Exception as e:
            success = False
            error_message = str(e)
    return render(request, "contact.html", {
        "hero_image": hero_image, 
        "form": form, 
        "success": success, 
        "error_message": error_message
    })


def categories_view(request):
    hero_image = PageHeroImage.objects.filter(page='categories', is_active=True).first()
    return render(request, "categories.html", {"categories": Category.objects.all(), "hero_image": hero_image})


def destinations(request):
    hero_image = PageHeroImage.objects.filter(page='destination', is_active=True).first()
    items = Destination.objects.all()
    return render(request, "destination.html", {"destinations": items, "hero_image": hero_image})


def destination_detail(request, slug: str):
    dest = get_object_or_404(Destination, slug=slug)
    return render(request, "destination_detail.html", {"destination": dest})


def post_detail(request, slug: str):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "post_detail.html", {"post": post})


def privacy_policy(request):
    return render(request, "privacy_policy.html")


def terms_and_conditions(request):
    return render(request, "terms_and_conditions.html")