from django.core.management.base import BaseCommand, CommandError
from mytig.models import Book, Word, Reference
from mytig.serializers import BookSerializer, WordSerializer, ReferenceSerializer

import time
from rest_framework.exceptions import ValidationError
import urllib.request
import re
from collections import defaultdict

class Command(BaseCommand):
    help = 'Loads list of books which are available.'

    def handle(self, *args, **options):
        if Word.objects.exists():
            Word.objects.all().delete()

        if Reference.objects.exists():
            Reference.objects.all().delete()

        self.stdout.write('['+time.ctime()+'] Loading data asked by...')
        words_per_book = []
    
        try:
            for book in Book.objects.all():
                bookSerializer = BookSerializer(book)
                url = bookSerializer.data['content']
                with urllib.request.urlopen(url) as response:
                    text = re.sub(r'[^\w\s]', '', response.read().decode('utf-8')).split("\n")

                dictionary = defaultdict(lambda: {'name': '', 'occurrence': 0, 'book':bookSerializer.data['id']})
        
                for line in text:
                    for word in line.split():
                        # eliminate words with less than 3 characters and those composed of only numbers

                        if not word.isdigit() or len(word) > 2:
                            dictionary[word.lower()]['name'] = word.lower()
                            dictionary[word.lower()]['occurrence'] += 1

                words_per_book += list(dictionary.values())

            sorted_list = sorted(words_per_book, key=lambda x: x['name'])

            mot = ""

            for item in sorted_list:
                if item['name'] != mot :
                    mot = item['name']
                    word_serializer = WordSerializer(data={
                        "token":mot
                    })
                    try:
                        word_serializer.is_valid(raise_exception=True)
                        word_serializer.save()
                    except ValidationError as e:
                        self.stdout.write('['+time.ctime()+']Error occurred while serializing word: '+str(e))
                        break
                word = Word.objects.latest('id')
                ser = WordSerializer(word)
                ref_serializer = ReferenceSerializer(data={
                    "word":ser.data['id'],
                    "book_reference": item['book'],
                    "occurrence": item['occurrence']
                })
                try:
                    ref_serializer.is_valid(raise_exception=True)
                    ref_serializer.save()
                except ValidationError as e:
                    self.stdout.write('['+time.ctime()+']Error occurred while serializing reference: '+str(e))
                    break

        except Exception as e:
           self.stdout.write('['+time.ctime()+"]An error occurred:", e)

        self.stdout.write('['+time.ctime()+'] Data refresh terminated. Thakn you for using Bogota.')
