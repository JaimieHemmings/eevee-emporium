from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    """A custom management command to check production settings."""
    help = 'Prints critical settings for debugging S3 deployment.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Checking Deployment Settings ---'))

        # Check if the USE_AWS environment variable is set
        use_aws = 'USE_AWS' in os.environ
        self.stdout.write(f"Environment variable 'USE_AWS' is set: {use_aws}")

        # Print the settings Django is actually using
        critical_settings = [
            'STATICFILES_STORAGE',
            'DEFAULT_FILE_STORAGE',
            'AWS_STORAGE_BUCKET_NAME',
            'AWS_S3_REGION_NAME',
            'AWS_S3_CUSTOM_DOMAIN',
        ]

        for setting_name in critical_settings:
            value = getattr(settings, setting_name, '!!! NOT SET IN DJANGO SETTINGS !!!')
            self.stdout.write(f'{setting_name}: {value}')

        self.stdout.write(self.style.SUCCESS('--- End of Settings Check ---'))