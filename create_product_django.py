import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WildTrackConnect.settings')
django.setup()
from store.models import Product
p = Product.objects.create(name='Automated Test Product', description='', price='9.99', stock=10)
print('created', p.id)
