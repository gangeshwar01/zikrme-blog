from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_GET

from .models import Post, Category, Destination, City, PageHeroImage, HomeMiniVideo
from .forms import CategoryForm, PostForm, DestinationForm, HeroImageForm, PageHeroImageForm, HomeMiniVideoForm, PasswordChangeCustomForm


staff_required = user_passes_test(lambda u: u.is_active and u.is_staff)


@staff_required
def dashboard(request):
    try:
        page_heroes = PageHeroImage.objects.all()
    except:
        page_heroes = []
    
    stats = {
        "posts": Post.objects.count(),
        "published": Post.objects.filter(is_published=True).count(),
        "featured": Post.objects.filter(is_featured=True).count(),
        "articles": Post.objects.filter(is_article=True).count(),
        "categories": Category.objects.count(),
        "destinations": Destination.objects.count(),
        "cities": City.objects.count(),
        "recent_posts": Post.objects.order_by("-created_at")[:7],
        "page_heroes": page_heroes,
        "home_mini_video": HomeMiniVideo.objects.filter(is_active=True).first(),
    }
    return render(request, "panel/dashboard.html", stats)


@login_required
def panel_root(request):
    # Redirect any logged-in user to dashboard. Non-staff will be blocked by decorator on dashboard.
    return redirect(reverse("panel_dashboard"))


@require_GET
def admin_logout_get(request):
    """Allow logging out via GET to satisfy the admin's logout link.
    Redirects back to admin login.
    """
    logout(request)
    return redirect("/admin/login/")


# -------- Tailwind CRUD: Categories ---------
@staff_required
def category_list(request):
    items = Category.objects.order_by("name")
    form = CategoryForm()
    return render(request, "panel/categories/list.html", {"items": items, "form": form})


@staff_required
@require_http_methods(["POST"])
def category_create(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect("panel_category_list")


@staff_required
def category_edit(request, pk: int):
    item = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("panel_category_list")
    else:
        form = CategoryForm(instance=item)
    return render(request, "panel/categories/edit.html", {"form": form, "item": item})


@staff_required
@require_http_methods(["POST"])
def category_delete(request, pk: int):
    item = get_object_or_404(Category, pk=pk)
    item.delete()
    return redirect("panel_category_list")


# -------- Tailwind CRUD: Posts ---------
@staff_required
def post_list(request):
    query = (request.GET.get("q") or "").strip()
    items_qs = Post.objects.order_by("-created_at")
    if query:
        items_qs = items_qs.filter(title__icontains=query)
    return render(request, "panel/posts/list.html", {"items": items_qs, "query": query})


@staff_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("panel_post_list")
    else:
        form = PostForm()
    return render(request, "panel/posts/form.html", {"form": form, "title": "Create Post"})


@staff_required
def post_edit(request, pk: int):
    item = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("panel_post_list")
    else:
        form = PostForm(instance=item)
    return render(request, "panel/posts/form.html", {"form": form, "title": "Edit Post", "item": item})


@staff_required
@require_http_methods(["POST"])
def post_delete(request, pk: int):
    item = get_object_or_404(Post, pk=pk)
    item.delete()
    return redirect("panel_post_list")


# -------- Tailwind CRUD: Destinations ---------
@staff_required
def destination_list(request):
    items = Destination.objects.order_by("title")
    form = DestinationForm()
    return render(request, "panel/destinations/list.html", {"items": items, "form": form})


@staff_required
@require_http_methods(["POST"])
def destination_create(request):
    form = DestinationForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    return redirect("panel_destination_list")


@staff_required
def destination_edit(request, pk: int):
    item = get_object_or_404(Destination, pk=pk)
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("panel_destination_list")
    else:
        form = DestinationForm(instance=item)
    return render(request, "panel/destinations/edit.html", {"form": form, "item": item})


@staff_required
@require_http_methods(["POST"])
def destination_delete(request, pk: int):
    item = get_object_or_404(Destination, pk=pk)
    item.delete()
    return redirect("panel_destination_list")


# -------- Tailwind CRUD: Hero Images ---------
@staff_required
def hero_list(request):
    items = HeroImage.objects.order_by("order")
    form = HeroImageForm()
    return render(request, "panel/hero/list.html", {"items": items, "form": form})


@staff_required
@require_http_methods(["POST"])
def hero_create(request):
    form = HeroImageForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    return redirect("panel_hero_list")


@staff_required
@require_http_methods(["POST"])
def hero_toggle(request, pk: int):
    item = get_object_or_404(HeroImage, pk=pk)
    item.is_active = not item.is_active
    item.save()
    return redirect("panel_hero_list")


# -------- Tailwind CRUD: Page Hero Images ---------
@staff_required
def page_hero_list(request):
    items = PageHeroImage.objects.order_by("page")
    
    # Get messages and clear them
    success_message = request.session.pop('success_message', None)
    error_message = request.session.pop('error_message', None)
    
    # Create a fresh form
    form = PageHeroImageForm()
    
    context = {
        "items": items, 
        "form": form,
        "success_message": success_message,
        "error_message": error_message,
    }
    
    return render(request, "panel/page_hero/list.html", context)


@staff_required
@require_http_methods(["POST"])
def page_hero_create(request):
    form = PageHeroImageForm(request.POST, request.FILES)
    
    if form.is_valid():
        try:
            page_hero = form.save()
            # Add success message to session
            request.session['success_message'] = f"Page Hero for {page_hero.get_page_display()} created successfully!"
        except Exception as e:
            request.session['error_message'] = f"Error creating page hero: {str(e)}"
    else:
        # Store error message only
        request.session['error_message'] = "Please correct the errors below."
    
    return redirect("panel_page_hero_list")


@staff_required
def page_hero_edit(request, pk: int):
    item = get_object_or_404(PageHeroImage, pk=pk)
    if request.method == "POST":
        form = PageHeroImageForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("panel_page_hero_list")
    else:
        form = PageHeroImageForm(instance=item)
    return render(request, "panel/page_hero/form.html", {"form": form, "title": "Edit Page Hero", "item": item})


@staff_required
@require_http_methods(["POST"])
def page_hero_delete(request, pk: int):
    item = get_object_or_404(PageHeroImage, pk=pk)
    item.delete()
    return redirect("panel_page_hero_list")


# -------- Home Mini Video Management ---------
@staff_required
def home_mini_video_list(request):
    items = HomeMiniVideo.objects.order_by("-created_at")
    form = HomeMiniVideoForm()
    return render(request, "panel/home_mini_video/list.html", {"items": items, "form": form})


@staff_required
@require_http_methods(["POST"])
def home_mini_video_create(request):
    form = HomeMiniVideoForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    return redirect("panel_home_mini_video_list")


@staff_required
def home_mini_video_edit(request, pk: int):
    item = get_object_or_404(HomeMiniVideo, pk=pk)
    if request.method == "POST":
        form = HomeMiniVideoForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("panel_home_mini_video_list")
    else:
        form = HomeMiniVideoForm(instance=item)
    return render(request, "panel/home_mini_video/form.html", {"form": form, "title": "Edit Home Mini Video", "item": item})


@staff_required
@require_http_methods(["POST"])
def home_mini_video_delete(request, pk: int):
    item = get_object_or_404(HomeMiniVideo, pk=pk)
    item.delete()
    return redirect("panel_home_mini_video_list")


# -------- Custom Password Change ---------
@staff_required
def password_change_custom(request):
    if request.method == "POST":
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["new_password"])
            request.user.save()
            from django.contrib import messages
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password updated successfully.")
            return redirect("panel_dashboard")
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, "panel/password_change.html", {"form": form, "title": "Change Password"})


