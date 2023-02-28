from rest_framework.serializers import ModelSerializer
from mytig.models import Book
from mytig.models import Word
from mytig.models import Reference

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'b_id', 'title', 'content', 'image')

class WordSerializer(ModelSerializer):
    class Meta:
        model = Word
        fields = ('id', 'token')

class ReferenceSerializer(ModelSerializer):
    class Meta:
        model = Reference
        fields = ('id', 'word', 'book_reference', 'occurrence' )

class JointureSerializer(ModelSerializer):
    book_reference = BookSerializer()
    word = WordSerializer()
    class Meta:
        model = Reference
        fields = ('id', 'word', 'book_reference', 'occurrence' )
