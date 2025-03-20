import random
from faker import Faker
from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = "generates test products for db"

    def handle(self, *args, **options):
        fake = Faker()

        categories = ["Cars", "Food", "Phones", "Computers", "Shoes", "Shirts"]
        categories_objects = [Category.objects.get_or_create(name=categorie) [0] for categorie in categories]

        Product.objects.all().delete()

        for _ in range(50):
            Product.objects.create(
                name = fake.word().capitalize(),
                category = random.choice(categories_objects),
                nomenclature = fake.unique.uuid4(),
                description = fake.text(max_nb_chars=200),
                price = random.randint(1,101),
                discount = random.randint(1,51),
                entity = random.randint(1,1001),
                available = random.choice([True, False]),
                rating = round(random.uniform(0.1, 5.0), 1),
                attributes = {
                    "colour": fake.color_name()
                              }
            )
    
        self.stdout.write(self.style.SUCCESS("Successufully added 50 products"))
