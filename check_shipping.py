from payment.models import ShippingAddress
from django.contrib.auth.models import User

print('Total ShippingAddress records:', ShippingAddress.objects.count())
for user in User.objects.all():
    count = ShippingAddress.objects.filter(user=user).count()
    print(f'User {user.username} has {count} shipping addresses')
    if count > 1:
        print(f'  - IDs: {list(ShippingAddress.objects.filter(user=user).values_list("id", flat=True))}')
