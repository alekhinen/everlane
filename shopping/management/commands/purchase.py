from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Purchases the product in the given user\'s shopping cart'

    def add_arguments(self, parser):
        parser.add_argument('user', type=int)

    def handle(self, *args, **options):
        user_id = options['user']

        try:
            user = User.objects.get(pk=user_id)
        except:
            raise CommandError('User {0} does not exist!'.format(user_id))

        try:
            purchase_history = user.shopping_cart.purchase()
        except:
            raise CommandError('Purchase could not be made for the cart!')

        success_message = 'Successfully purchased products.'
        self.stdout.write(self.style.SUCCESS(success_message))
