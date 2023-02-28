from rest_framework.views import APIView
from rest_framework.response import Response
from mytig.config import baseUrl
import requests

from mytig.models import Book,Word,Reference
from mytig.serializers import BookSerializer,WordSerializer,JointureSerializer
from mytig.methods import Autocomplete, asc, reconstruct

from operator import itemgetter
import urllib.request

# Create your views here.
class ListeDeLivres(APIView):
    def get(self, request, format=None):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
#    def post(self, request, format=None):
#        NO DEFITION of post --> server will return "405 NOT ALLOWED"

class DetailLivre(APIView):
    def get(self, request, pk, format=None):
        try:
            if Book.objects.filter(b_id = str(pk)).exists():
                params = {
                    "ids": pk,
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.get(baseUrl, params=params, headers=headers)

                data = response.json()['results'][0]

                with urllib.request.urlopen(data['formats']['text/html']) as content:
                    html = content.read().decode('utf-8')


                data = dict(
                    title = data['title'], 
                    image = data['formats']['image/jpeg'], 
                    authors = ' | '.join(list(map(itemgetter('name'), data['authors']))), 
                    translators = ' | '.join(list(map(itemgetter('name'), data['translators']))),
                    subjects = ' | '.join(data['subjects']), 
                    bookShelves = ' | '.join(data['bookshelves']),
                    languages =  ' | '.join(data['languages']),
                    html = html,
                    )

                return Response(data)
            else:
                raise Exception
        except:
            raise Http404
#    def put(self, request, pk, format=None):
#        NO DEFITION of put --> server will return "405 NOT ALLOWED"
#    def delete(self, request, pk, format=None):
#        NO DEFITION of delete --> server will return "405 NOT ALLOWED"

class Suggestion(APIView):
    def get(self, request, search, format=None):
        words = Word.objects.all()
        serializer = WordSerializer(words, many=True)

        words_list = list(map(itemgetter('token'), serializer.data))

        search = search.lower()
        Results = dict(founded = [], similar = [])
        max_distance = 1 #distance maximale pour l'auto correcteur
        autocomplete = Autocomplete(words_list)
        Results['founded'] = autocomplete.autocomplete(search)
        if len(Results['founded']) == 0:
            Results['similar'] = asc(search,words_list,max_distance)
        return Response(Results) 
    
class FindWord(APIView):
    def get(self, request, search, format=None):

        word = get_object_or_404(Word, token=search)

        references = Reference.objects.select_related('book_reference').filter(word=word)
        refSerializer = JointureSerializer(references, many = True)

        result = list(map(reconstruct, refSerializer.data))


        # results = dict(refSerializer.data['book_reference'])

        # results['occurrence'] = refSerializer.data['occurrence']

        return Response(result) 
    
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Word, Book, Reference

