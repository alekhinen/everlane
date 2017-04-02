from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Adds the given product to the given user\'s shopping cart'

    def add_arguments(self, parser):
        parser.add_argument('user', type=int)
        parser.add_argument('product', type=int)
        parser.add_argument('quantity', type=int)

    def handle(self, *args, **options):
        quantity = options['quantity']
        user_id = options['user']
        product_id = options['product']

        try:
            user = User.objects.get(pk=user_id)
        except:
            raise CommandError('User {0} does not exist!'.format(user_id))

        try:
            products = user.shopping_cart.add_product(product_id, quantity=quantity)
        except:
            raise CommandError('Product {0} cannot be added to the cart!'.format(product_id))

        success_message = 'Added {0} products for a total of {1} in the cart.'.format(quantity, len(products))
        self.stdout.write(self.style.SUCCESS(success_message))
