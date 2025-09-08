from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import Category, Post, Destination, City, CityMedia, HeroImage, PageHeroImage, HomeMiniVideo


class BaseTailwindForm(forms.ModelForm):
    def _apply_tailwind(self):
        for field_name, field in self.fields.items():
            widget = field.widget
            css = widget.attrs.get("class", "")
            widget.attrs["class"] = (
                css
                + " w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            ).strip()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_tailwind()


class CategoryForm(BaseTailwindForm):
    class Meta:
        model = Category
        fields = ["name", "icon_class", "show_in_footer"]


class PostForm(BaseTailwindForm):
    published_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "description",
            "image",
            "youtube_url",
            "external_link",
            "categories",
            "is_published",
            "is_featured",
            "is_article",
            "published_at",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "categories": forms.SelectMultiple(
                attrs={"class": "w-full rounded-lg border border-slate-300"}
            ),
        }


class DestinationForm(BaseTailwindForm):
    class Meta:
        model = Destination
        fields = ["title", "description", "hero_image", "mini_video"]
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}


class CityForm(BaseTailwindForm):
    class Meta:
        model = City
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}


class CityMediaForm(BaseTailwindForm):
    class Meta:
        model = CityMedia
        fields = ["image", "youtube_url"]


class HeroImageForm(BaseTailwindForm):
    class Meta:
        model = HeroImage
        fields = ["image", "caption", "is_active"]


class PageHeroImageForm(BaseTailwindForm):
    class Meta:
        model = PageHeroImage
        fields = ["page", "image", "title", "subtitle", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter hero title"}),
            "subtitle": forms.TextInput(attrs={"placeholder": "Enter hero subtitle"}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        page = cleaned_data.get('page')
        image = cleaned_data.get('image')
        
        # Check if page already has a hero image
        if page and not self.instance.pk:  # Only check on creation, not edit
            if PageHeroImage.objects.filter(page=page).exists():
                # Get the display name for the page
                page_choices = dict(PageHeroImage.PAGE_CHOICES)
                page_display = page_choices.get(page, page)
                raise forms.ValidationError(f"A hero image for {page_display} already exists.")
        
        # Ensure image is provided
        if not image:
            raise forms.ValidationError("Please select an image for the hero section.")
        
        return cleaned_data


class HomeMiniVideoForm(BaseTailwindForm):
    class Meta:
        model = HomeMiniVideo
        fields = ["video_file", "youtube_url", "is_active", "autoplay", "muted"]
        widgets = {
            "youtube_url": forms.URLInput(attrs={"placeholder": "https://www.youtube.com/watch?v=..."}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        video_file = cleaned_data.get('video_file')
        youtube_url = cleaned_data.get('youtube_url')
        
        # Ensure at least one video source is provided
        if not video_file and not youtube_url:
            raise forms.ValidationError("Please provide either a video file or YouTube URL.")
        
        # Don't allow both
        if video_file and youtube_url:
            raise forms.ValidationError("Please provide either a video file OR YouTube URL, not both.")
        
        return cleaned_data


class TailwindForm(forms.Form):
    def _apply_tailwind(self):
        for field_name, field in self.fields.items():
            widget = field.widget
            css = widget.attrs.get("class", "")
            widget.attrs["class"] = (
                css
                + " w-full px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            ).strip()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_tailwind()


class PasswordChangeCustomForm(TailwindForm):
    current_password = forms.CharField(widget=forms.PasswordInput, label="Current password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm new password")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        pwd = self.cleaned_data.get("current_password")
        if not self.user.check_password(pwd):
            raise forms.ValidationError("Current password is incorrect.")
        return pwd

    def clean_new_password(self):
        pwd = self.cleaned_data.get("new_password")
        validate_password(pwd, self.user)
        return pwd

    def clean(self):
        cleaned = super().clean()
        np = cleaned.get("new_password")
        cp = cleaned.get("confirm_password")
        if np and cp and np != cp:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned


class ContactForm(TailwindForm):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 6}))

