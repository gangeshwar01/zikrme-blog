from django.contrib.admin import AdminSite


class ZikRmeAdminSite(AdminSite):
    site_header = "ZikRme Admin Panel"
    site_title = "ZikRme Admin"
    index_title = "Dashboard"
    login_template = "admin/custom_login.html"
    index_template = "admin/panel/index.html"

    def index(self, request, extra_context=None):  # type: ignore[override]
        try:
            from .models import Post, Category, Destination, City, PageHeroImage
            print(f"DEBUG: Successfully imported PageHeroImage: {PageHeroImage}")  # Debug print
            
            page_heroes = PageHeroImage.objects.all()
            print(f"DEBUG: Found {page_heroes.count()} page heroes")  # Debug print
            
            stats = {
                "posts": Post.objects.count(),
                "published": Post.objects.filter(is_published=True).count(),
                "featured": Post.objects.filter(is_featured=True).count(),
                "articles": Post.objects.filter(is_article=True).count(),
                "categories": Category.objects.count(),
                "destinations": Destination.objects.count(),
                "cities": City.objects.count(),
                "recent_posts": Post.objects.order_by("-created_at")[:5],
                "page_heroes": page_heroes,
            }
            extra = extra_context or {}
            extra.update(stats)
            return super().index(request, extra_context=extra)
        except Exception as e:
            print(f"DEBUG ERROR: {e}")  # Debug print
            # Fallback if there's an error
            from .models import Post, Category, Destination, City
            
            stats = {
                "posts": Post.objects.count(),
                "published": Post.objects.filter(is_published=True).count(),
                "featured": Post.objects.filter(is_featured=True).count(),
                "articles": Post.objects.filter(is_article=True).count(),
                "categories": Category.objects.count(),
                "destinations": Destination.objects.count(),
                "cities": City.objects.count(),
                "recent_posts": Post.objects.order_by("-created_at")[:5],
                "page_heroes": [],
                "debug_error": str(e),
            }
            extra = extra_context or {}
            extra.update(stats)
            return super().index(request, extra_context=extra)


custom_admin_site = ZikRmeAdminSite(name="panel")

# Reuse existing ModelAdmin classes defined in zikrmeblogapp.admin
from .models import Category, HeroImage, Post, Destination, City, PageHeroImage  # noqa: E402
from .admin import (  # noqa: E402
    CategoryAdmin,
    HeroImageAdmin,
    PostAdmin,
    DestinationAdmin,
    CityAdmin,
    PageHeroImageAdmin,
)

custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(HeroImage, HeroImageAdmin)
custom_admin_site.register(Post, PostAdmin)
custom_admin_site.register(Destination, DestinationAdmin)
custom_admin_site.register(City, CityAdmin)
custom_admin_site.register(PageHeroImage, PageHeroImageAdmin)


