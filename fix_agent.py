import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realstate.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Agent
from listings.models import Listing
from django.db.models.signals import post_save
from accounts.signals import agent_post_save

# Signal temporär deaktivieren
post_save.disconnect(agent_post_save, sender=Agent)

user, _ = User.objects.get_or_create(username='testmakler')
agent = Agent.objects.create(user=user, first_name='Max', last_name='Mustermann')
print(f'Agent ID: {agent.id}')

for l in Listing.objects.all():
    l.realtor = agent
    l.save()
    print(f'OK: {l.property_title}')

print('Fertig!')
