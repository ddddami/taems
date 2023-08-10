from django.core.management.base import BaseCommand
from core.models import User
import random


class Command(BaseCommand):
    help = 'Create a thousand users'

    def handle(self, *args, **options):
        first_names = [
            "John", "Jane", "Michael", "Emily", "Robert", "Karen", "David", "Jennifer",
            "William", "Linda", "James", "Patricia", "Charles", "Elizabeth", "George", "Mary",
            "Mark", "Barbara", "Joseph", "Susan", "Richard", "Dorothy", "Thomas", "Margaret",
            "Daniel", "Lisa", "Paul", "Betty", "Steven", "Dorothy", "Kenneth", "Sarah",
            "Edward", "Karen", "Brian", "Nancy", "Ronald", "Karen", "Anthony", "Sandra",
            "Kevin", "Ashley", "Jason", "Kimberly", "Matthew", "Donna", "Gary", "Carol",
            "Timothy", "Michelle", "Jose", "Emily", "Larry", "Amanda", "Jeffrey", "Melissa",
            "Frank", "Deborah", "Scott", "Stephanie", "Eric", "Rebecca", "Stephen", "Laura",
            "Andrew", "Helen", "Raymond", "Sharon", "Gregory", "Cynthia", "Joshua", "Kathleen",
            "Jerry", "Amy", "Dennis", "Shirley", "Walter", "Angela", "Patrick", "Anna",
            "Peter", "Ruth", "Harold", "Brenda", "Douglas", "Pamela", "Henry", "Nicole",
            "Carl", "Christine", "Arthur", "Catherine", "Ryan", "Virginia", "Roger", "Debra",
            # Add more first names here
        ]

        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore",
            "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson",
            "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker",
            "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott",
            "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez",
            "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins",
            "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy",
            "Bailey", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson",
            "Gray", "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders", "Price",
            "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman", "Jenkins", "Perry",
            # Add more last names here
        ]

        for i in range(1000):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}_{i}@example.com".replace(" ", "_")
            password = 'ILoveDjango'

            User.objects.create_user(
                username=f"user_{i}",
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

        self.stdout.write(self.style.SUCCESS('Successfully created users'))
