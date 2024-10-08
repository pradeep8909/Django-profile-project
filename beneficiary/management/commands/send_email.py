from django.core.management.base import BaseCommand
from beneficiary.models import Beneficiary
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class Command(BaseCommand):
    help = "Send an email using Django's email functionality"

    def handle(self, *args, **kwargs):
        subject = "Total Number of Beneficiaries "
        beneficiary_count = Beneficiary.objects.count()

        # Create an HTML horizontal table with double borders
        message = f"""
        <html>
        <body>
            <p><strong>Total number of beneficiaries registered till now:</strong></p>
            <table border="2" cellpadding="10" cellspacing="0" style="border: 3px double black; border-collapse: collapse;">
                <tr>
                    <td style="border: 3px double black;"><strong>Total Beneficiaries</strong></td>
                    <td style="border: 3px double black;">{beneficiary_count}</td>
                </tr>
            </table>
        </body>
        </html>
        """

        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['anurag18@navgurukul.org', 'pradeep18@navgurukul.org']

        try:
            email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
            email.attach_alternative(message, "text/html")
            email.send()
            self.stdout.write(self.style.SUCCESS('Successfully sent email with beneficiary count!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
