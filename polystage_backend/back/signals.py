
from django_cas_ng.signals import cas_user_authenticated
from django.dispatch import receiver

@receiver(cas_user_authenticated)
def cas_user_authenticated_callback(sender, user, created, attributes, ticket, **kwargs):
    # Récupérez la session à partir de kwargs
    session = kwargs.get('session')

    # Assurez-vous que la session est modifiable
    if session is None or not session.session_key:
        raise ValueError("Session is not available or invalid")

    # Stockez le ticket et les attributs dans la session
    session['ticket'] = ticket
    session['attributes'] = attributes
    print("bonjour")
    session.save()