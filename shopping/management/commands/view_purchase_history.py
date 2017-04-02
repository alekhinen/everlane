from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'View the purchase history of the given user'

    def add_arguments(self, parser):
        parser.add_argument('user', type=int)

    def handle(self, *args, **options):
        user_id = options['user']

        try:
            user = User.objects.get(pk=user_id)
        except:
            raise CommandError('User {0} does not exist!'.format(user_id))

        # build out the print out of purchase histories
        success_message = ""
        purchase_histories = user.purchase_history.all()
        for purchase_history in purchase_histories:
            success_message += purchase_history.to_string()

        self.stdout.write(self.style.SUCCESS(success_message))
