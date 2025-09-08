from django.db import models
from django.utils.text import slugify
import math


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    icon_class = models.CharField(
        max_length=80,
        blank=True,
        help_text="CSS class for an icon (e.g. 'ri-earth-line' or 'fa fa-map-marker').",
    )
    show_in_footer = models.BooleanField(default=False, help_text="Show this category in the site footer")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class HeroImage(TimeStampedModel):
    image = models.FileField(upload_to="hero/")
    caption = models.CharField(max_length=180, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of display in slider (lower numbers appear first)")

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self) -> str:
        return self.caption or f"Hero {self.pk}"


class PageHeroImage(TimeStampedModel):
    PAGE_CHOICES = [
        ('categories', 'Categories Page'),
        ('destination', 'Destination Page'),
        ('about', 'About Page'),
        ('contact', 'Contact Page'),
    ]
    
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    image = models.FileField(upload_to="page_hero/")
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['page']

    def __str__(self) -> str:
        return f"{self.get_page_display()} Hero"


class HomeMiniVideo(TimeStampedModel):
    video_file = models.FileField(upload_to="home/video/", blank=True, null=True, help_text="Upload a video file")
    youtube_url = models.URLField(blank=True, help_text="Or provide a YouTube URL")
    is_active = models.BooleanField(default=True)
    autoplay = models.BooleanField(default=True, help_text="Auto-play the video")
    muted = models.BooleanField(default=True, help_text="Start video muted")

    class Meta:
        verbose_name = "Home Mini Video"
        verbose_name_plural = "Home Mini Videos"

    def __str__(self) -> str:
        return f"Home Mini Video ({'Active' if self.is_active else 'Inactive'})"


class Post(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    image = models.FileField(upload_to="posts/", blank=True, null=True)
    youtube_url = models.URLField(blank=True)
    external_link = models.URLField(blank=True, help_text="Optional link for more details")
    categories = models.ManyToManyField(Category, related_name="posts", blank=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_article = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @property
    def estimated_read_minutes(self) -> int:
        """Estimate read time based on description word count (~200 wpm)."""
        if not self.description:
            return 1
        words = len(self.description.split())
        return max(1, math.ceil(words / 200))


class PostLink(TimeStampedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="links",
    )
    label = models.CharField(max_length=80)
    url = models.URLField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.label}"


class Destination(TimeStampedModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField(blank=True)
    hero_image = models.FileField(upload_to="destinations/hero/", blank=True, null=True)
    mini_video = models.FileField(upload_to="destinations/video/", blank=True, null=True)

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class City(TimeStampedModel):
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name="cities"
    )
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("destination", "slug")
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.destination.title})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class CityMedia(TimeStampedModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="media")
    image = models.FileField(upload_to="destinations/", blank=True, null=True)
    youtube_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return f"Media for {self.city.name}"

