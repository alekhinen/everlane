from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Removes the given product to the given user\'s shopping cart'

    def add_arguments(self, parser):
        parser.add_argument('user', type=int)
        parser.add_argument('product', type=int)

    def handle(self, *args, **options):
        user_id = options['user']
        product_id = options['product']

        try:
            user = User.objects.get(pk=user_id)
        except:
            raise CommandError('User {0} does not exist!'.format(user_id))

        try:
            products = user.shopping_cart.remove_product(product_id)
        except:
            raise CommandError('Product {0} cannot be added to the cart!'.format(product_id))

        success_message = 'Removed product for a total of {0} in the cart.'.format(len(products))
        self.stdout.write(self.style.SUCCESS(success_message))
