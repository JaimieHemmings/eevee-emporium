from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payment.models import ShippingAddress
from django.db import transaction


class Command(BaseCommand):
    help = 'Clean up duplicate ShippingAddress records, keeping the most recent one for each user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        deleted_count = 0
        
        for user in User.objects.all():
            # Get all shipping addresses for this user, ordered by most recent first
            addresses = ShippingAddress.objects.filter(user=user).order_by('-updated_at', '-created_at', '-id')
            
            if addresses.count() > 1:
                # Keep the first (most recent) address and delete the rest
                keep_address = addresses.first()
                delete_addresses = addresses[1:]
                
                self.stdout.write(
                    f'User {user.username} has {addresses.count()} shipping addresses'
                )
                self.stdout.write(
                    f'  Keeping address ID {keep_address.id} (updated: {keep_address.updated_at})'
                )
                
                for addr in delete_addresses:
                    self.stdout.write(
                        f'  {"Would delete" if dry_run else "Deleting"} address ID {addr.id} (updated: {addr.updated_at})'
                    )
                    if not dry_run:
                        addr.delete()
                        deleted_count += 1
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'DRY RUN: Would delete {sum(ShippingAddress.objects.filter(user=u).count() - 1 for u in User.objects.all() if ShippingAddress.objects.filter(user=u).count() > 1)} duplicate addresses')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {deleted_count} duplicate shipping addresses')
            )
