"""
Data Migration Script: Migrate Agent data to Professional model.
Run this once to transfer all existing Agent records.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, '/app/real-estate-django-main')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realstate.settings')
django.setup()

from accounts.models import Agent
from main.professional_models import Professional
from listings.models import Listing


def migrate_agents_to_professionals():
    """Migrate all Agent records to Professional model."""
    
    agents = Agent.objects.all()
    migrated_count = 0
    
    print(f"\n=== Migrating {agents.count()} Agent(s) to Professional ===\n")
    
    for agent in agents:
        # Check if already migrated (by user relationship)
        if agent.user and Professional.objects.filter(user=agent.user).exists():
            print(f"  SKIP: {agent.first_name} {agent.last_name} - already migrated")
            continue
        
        # Create Professional record
        name = f"{agent.first_name or ''} {agent.last_name or ''}".strip()
        if not name and agent.company_name:
            name = agent.company_name
        elif not name:
            name = f"Agent-{str(agent.id)[:8]}"
        
        professional = Professional.objects.create(
            user=agent.user,
            professional_type='real_estate_agent',  # Default to Makler
            name=name,
            email=agent.email or (agent.user.email if agent.user else ''),
            phone=agent.mobile,
            mobile=agent.mobile,
            fax=agent.fax,
            city=agent.city,
            country=agent.country or 'Kroatien',
            company_name=agent.company_name,
            company_logo=agent.company_logo,
            profile_image=agent.profile_image,
            portrait_photo=agent.portrait_photo,
            oib_number=agent.oib_number,
            website=agent.domain,
            description=agent.description,
            description_de=agent.description_de or agent.description,
            description_hr=agent.description_hr,
            facebook=agent.facebook,
            instagram=agent.instagram,
            linkedin=agent.linkedin,
            twitter=agent.twitter,
            youtube=agent.youtube,
            is_active=agent.is_active,
            is_verified=agent.is_active,  # If active, assume verified
        )
        
        # Update related Listings to point to new Professional
        listings_updated = Listing.objects.filter(realtor=agent).update(professional=professional)
        
        print(f"  OK: {name} -> Professional (ID: {professional.id})")
        print(f"      - {listings_updated} Listing(s) updated")
        migrated_count += 1
    
    print(f"\n=== Migration complete: {migrated_count} Agent(s) migrated ===\n")
    return migrated_count


if __name__ == '__main__':
    migrate_agents_to_professionals()
