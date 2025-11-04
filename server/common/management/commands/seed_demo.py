from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from project_tracker.models import Board, Column, Card
from shop.models import Product
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        u,_=User.objects.get_or_create(username="demo",defaults={"email":"demo@example.com"})
        u.set_password("demo1234"); u.save()
        b,_=Board.objects.get_or_create(owner=u,name="Demo Board")
        todo,_=Column.objects.get_or_create(board=b,name="Todo",position=0)
        doing,_=Column.objects.get_or_create(board=b,name="Doing",position=1)
        done,_=Column.objects.get_or_create(board=b,name="Done",position=2)
        Card.objects.get_or_create(column=todo,title="Wire UI",position=0)
        Card.objects.get_or_create(column=doing,title="Build API",position=0)
        Card.objects.get_or_create(column=done,title="Write README",position=0)
        Product.objects.get_or_create(name="Pro Plan",price_cents=9900,active=True)
        Product.objects.get_or_create(name="Consultation",price_cents=19900,active=True)
        self.stdout.write(self.style.SUCCESS("Seeded demo data (user: demo / pass: demo1234)"))
