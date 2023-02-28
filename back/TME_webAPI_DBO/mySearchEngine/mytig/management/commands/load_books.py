from django.core.management.base import BaseCommand, CommandError
from mytig.models import Book
from mytig.serializers import BookSerializer
from mytig.config import baseUrl
import requests
import time
from rest_framework.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Loads list of books which are available.'

    def handle(self, *args, **options):
        if Book.objects.exists():
            Book.objects.all().delete()
            
        self.stdout.write('['+time.ctime()+'] Loading data asked by...')
        params = {
            "mime_type": "image/jpeg",
            "page": 1,
        }
                
        for i in range(54):
            response = requests.get(baseUrl, params=params)
            if response.status_code != 200:
                self.stdout.write('['+time.ctime()+"]Error occurred while retrieving data.")
                break
            
            data = response.json()['results']
            if not data:
                break
            
            for book in data:
                if 'text/plain' in book['formats']:
                    serializer = BookSerializer(data={
                        "b_id":str(book['id']),
                        "title": book['title'],
                        "content": book['formats']['text/plain'],
                        "image": book['formats']['image/jpeg']
                    })
                    try:
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        self.stdout.write(self.style.SUCCESS('['+time.ctime()+'] Successfully added book id="%s"' % book['id']))
                    except ValidationError as e:
                        self.stdout.write('['+time.ctime()+']Error occurred while serializing data: '+str(e))
                        break

            params["page"] += 1
        self.stdout.write('['+time.ctime()+'] Data refresh terminated. Thakn you for using Bogota.')
