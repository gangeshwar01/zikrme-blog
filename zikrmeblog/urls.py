"""
URL configuration for zikrmeblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from zikrmeblogapp import views as app_views
from zikrmeblogapp.admin_site import custom_admin_site
from zikrmeblogapp import panel_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Auth fallbacks for panel
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Override admin login to ensure our template and correct redirects
    path(
        "admin/login/",
        auth_views.LoginView.as_view(
            template_name="admin/custom_login.html",
            redirect_authenticated_user=True,
        ),
        name="admin_login_override",
    ),
    # Allow GET logout for admin link
    path("admin/logout/", panel_views.admin_logout_get, name="admin_logout_get"),
    # Django admin (after explicit admin/logout/ so our route wins)
    path("admin/", admin.site.urls),
    # Tailwind custom panel UI
    path("panel/", panel_views.panel_root, name="panel_root"),
    path("panel/dashboard/", panel_views.dashboard, name="panel_dashboard"),
    # CRUD - Categories
    path("panel/categories/", panel_views.category_list, name="panel_category_list"),
    path("panel/categories/create/", panel_views.category_create, name="panel_category_create"),
    path("panel/categories/<int:pk>/edit/", panel_views.category_edit, name="panel_category_edit"),
    path("panel/categories/<int:pk>/delete/", panel_views.category_delete, name="panel_category_delete"),
    # CRUD - Posts
    path("panel/posts/", panel_views.post_list, name="panel_post_list"),
    path("panel/posts/create/", panel_views.post_create, name="panel_post_create"),
    path("panel/posts/<int:pk>/edit/", panel_views.post_edit, name="panel_post_edit"),
    path("panel/posts/<int:pk>/delete/", panel_views.post_delete, name="panel_post_delete"),
    # CRUD - Destinations
    path("panel/destinations/", panel_views.destination_list, name="panel_destination_list"),
    path("panel/destinations/create/", panel_views.destination_create, name="panel_destination_create"),
    path("panel/destinations/<int:pk>/edit/", panel_views.destination_edit, name="panel_destination_edit"),
    path("panel/destinations/<int:pk>/delete/", panel_views.destination_delete, name="panel_destination_delete"),
    # CRUD - Hero Images
    path("panel/hero/", panel_views.hero_list, name="panel_hero_list"),
    path("panel/hero/create/", panel_views.hero_create, name="panel_hero_create"),
    path("panel/hero/<int:pk>/toggle/", panel_views.hero_toggle, name="panel_hero_toggle"),
    # CRUD - Page Hero Images
    path("panel/page-hero/", panel_views.page_hero_list, name="panel_page_hero_list"),
    path("panel/page-hero/create/", panel_views.page_hero_create, name="panel_page_hero_create"),
    path("panel/page-hero/<int:pk>/edit/", panel_views.page_hero_edit, name="panel_page_hero_edit"),
    path("panel/page-hero/<int:pk>/delete/", panel_views.page_hero_delete, name="panel_page_hero_delete"),
    # Custom password change (panel)
    path("panel/password/change/", panel_views.password_change_custom, name="panel_password_change"),
    # CRUD - Home Mini Video
    path("panel/home-mini-video/", panel_views.home_mini_video_list, name="panel_home_mini_video_list"),
    path("panel/home-mini-video/create/", panel_views.home_mini_video_create, name="panel_home_mini_video_create"),
    path("panel/home-mini-video/<int:pk>/edit/", panel_views.home_mini_video_edit, name="panel_home_mini_video_edit"),
    path("panel/home-mini-video/<int:pk>/delete/", panel_views.home_mini_video_delete, name="panel_home_mini_video_delete"),
    path("", app_views.home, name="home"),
    path("about/", app_views.about, name="about"),
    path("contact/", app_views.contact, name="contact"),
    path("categories/", app_views.categories_view, name="categories"),
    path("destination/", app_views.destinations, name="destination"),
    path("destination/<slug:slug>/", app_views.destination_detail, name="destination_detail"),
    path("blogs/", app_views.posts_list, name="posts_list"),
    path("blog/<slug:slug>/", app_views.post_detail, name="post_detail"),
    path("category/<slug:slug>/", app_views.posts_by_category, name="posts_by_category"),
    path("featured/", app_views.featured_list, name="featured_list"),
    path("articles/", app_views.articles_list, name="articles_list"),
    path("privacy-policy/", app_views.privacy_policy, name="privacy_policy"),
    path("terms/", app_views.terms_and_conditions, name="terms_and_conditions"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
