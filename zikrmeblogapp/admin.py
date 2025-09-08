from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Category, HeroImage, Post, Destination, City, CityMedia, PageHeroImage, PostLink


class BulkHeroImageUploadForm:
    """Custom form for bulk hero image uploads"""
    def __init__(self, request=None):
        self.request = request

    def is_valid(self):
        return True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon_class", "show_in_footer", "created_at")
    list_editable = ("show_in_footer",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "image_preview", "order", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    list_editable = ("order", "is_active")
    search_fields = ("caption",)
    ordering = ("order", "created_at")
    actions = ["activate_all", "deactivate_all"]
    
    fieldsets = (
        (None, {
            "fields": ("image", "caption", "order", "is_active")
        }),
    )
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view), name='heroimage_bulk_upload'),
        ]
        return custom_urls + urls
    
    def bulk_upload_view(self, request):
        if request.method == 'POST':
            files = request.FILES.getlist('images')
            captions = request.POST.getlist('captions')
            
            if files:
                for i, file in enumerate(files):
                    if file:
                        caption = captions[i] if i < len(captions) else ""
                        # Get the next order number
                        next_order = HeroImage.objects.count()
                        HeroImage.objects.create(
                            image=file,
                            caption=caption,
                            order=next_order,
                            is_active=True
                        )
                
                messages.success(request, f"Successfully uploaded {len(files)} hero images.")
                return HttpResponseRedirect(reverse('admin:zikrmeblogapp_heroimage_changelist'))
        
        context = {
            'title': 'Bulk Upload Hero Images',
            'opts': self.model._meta,
            'form': BulkHeroImageUploadForm(),
        }
        return render(request, 'admin/heroimage_bulk_upload.html', context)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_bulk_upload'] = True
        return super().changelist_view(request, extra_context)
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 100px;" />'
        return "No image"
    image_preview.short_description = "Preview"
    image_preview.allow_tags = True
    
    def activate_all(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} hero images activated.")
    activate_all.short_description = "Activate selected images"
    
    def deactivate_all(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} hero images deactivated.")
    deactivate_all.short_description = "Deactivate selected images"


class CityMediaInline(admin.TabularInline):
    model = CityMedia
    extra = 1


class PostLinkInline(admin.TabularInline):
    model = PostLink
    extra = 1

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "destination", "slug")
    list_filter = ("destination",)
    inlines = [CityMediaInline]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_published",
        "is_featured",
        "is_article",
        "published_at",
    )
    list_filter = ("is_published", "is_featured", "is_article", "categories")
    search_fields = ("title", "description")
    filter_horizontal = ("categories",)
    inlines = [PostLinkInline]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "description")} ),
        (
            "Media & Links",
            {"fields": ("image", "youtube_url", "external_link")},
        ),
        (
            "Classification",
            {"fields": ("categories", "is_published", "is_featured", "is_article", "published_at")},
        ),
    )


@admin.register(PageHeroImage)
class PageHeroImageAdmin(admin.ModelAdmin):
    list_display = ("page", "title", "is_active", "created_at")
    list_filter = ("is_active", "page")
    list_editable = ("is_active",)
    search_fields = ("title", "subtitle")
    ordering = ("page",)
    
    fieldsets = (
        (None, {
            "fields": ("page", "image", "title", "subtitle", "is_active")
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow adding if there are less than 4 page hero images
        return PageHeroImage.objects.count() < 4

