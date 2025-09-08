from django.core.management.base import BaseCommand
from zikrmeblogapp.models import PageHeroImage


class Command(BaseCommand):
    help = 'Set up default page hero images for all pages'

    def handle(self, *args, **options):
        # Define default page hero configurations
        page_configs = [
            {
                'page': 'categories',
                'title': 'Explore Categories',
                'subtitle': 'Discover content organized by topics and interests'
            },
            {
                'page': 'destination',
                'title': 'Amazing Destinations',
                'subtitle': 'Explore incredible places around the world'
            },
            {
                'page': 'about',
                'title': 'About ZikRme',
                'subtitle': 'Your gateway to extraordinary travel experiences'
            },
            {
                'page': 'contact',
                'title': 'Get in Touch',
                'subtitle': 'We\'d love to hear from you'
            }
        ]

        created_count = 0
        for config in page_configs:
            # Check if page hero already exists
            if not PageHeroImage.objects.filter(page=config['page']).exists():
                PageHeroImage.objects.create(
                    page=config['page'],
                    title=config['title'],
                    subtitle=config['subtitle'],
                    is_active=False  # Set to False so admin can add images first
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created {config["page"]} page hero')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'{config["page"]} page hero already exists')
                )

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} page hero configurations')
            )
            self.stdout.write(
                self.style.WARNING(
                    'Note: All page heroes are set to inactive. '
                    'Go to admin panel > Page Hero Images to upload images and activate them.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('All page hero configurations already exist')
            )
