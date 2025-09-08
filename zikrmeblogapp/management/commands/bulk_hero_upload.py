from django.core.management.base import BaseCommand
from django.core.files import File
from zikrmeblogapp.models import HeroImage
import os
import glob


class Command(BaseCommand):
    help = 'Bulk upload hero images from a directory'

    def add_arguments(self, parser):
        parser.add_argument(
            'directory',
            type=str,
            help='Directory containing hero images'
        )
        parser.add_argument(
            '--caption-prefix',
            type=str,
            default='Hero Image',
            help='Prefix for image captions'
        )
        parser.add_argument(
            '--activate',
            action='store_true',
            help='Activate uploaded images'
        )

    def handle(self, *args, **options):
        directory = options['directory']
        caption_prefix = options['caption_prefix']
        activate = options['activate']

        if not os.path.exists(directory):
            self.stdout.write(
                self.style.ERROR(f'Directory {directory} does not exist')
            )
            return

        # Supported image extensions
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']
        image_files = []

        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(directory, ext)))
            image_files.extend(glob.glob(os.path.join(directory, ext.upper())))

        if not image_files:
            self.stdout.write(
                self.style.WARNING(f'No image files found in {directory}')
            )
            return

        # Sort files for consistent ordering
        image_files.sort()

        # Get current count for ordering
        current_count = HeroImage.objects.count()

        uploaded_count = 0
        for i, image_path in enumerate(image_files):
            try:
                filename = os.path.basename(image_path)
                caption = f"{caption_prefix} {i + 1}"

                # Check if image already exists
                if HeroImage.objects.filter(image__endswith=filename).exists():
                    self.stdout.write(
                        self.style.WARNING(f'Image {filename} already exists, skipping')
                    )
                    continue

                with open(image_path, 'rb') as f:
                    hero_image = HeroImage(
                        image=File(f, name=filename),
                        caption=caption,
                        order=current_count + i,
                        is_active=activate
                    )
                    hero_image.save()
                    uploaded_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Uploaded {filename}')
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error uploading {image_path}: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully uploaded {uploaded_count} hero images'
            )
        )
