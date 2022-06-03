from django.http import HttpRequest
from .json_rpc_api import api
from .models import Book
from .serializers import BookSerializer


@api.dispatcher.add_method(name='utils.sum')
def _sum(request, *args, **kwargs):
    return sum(args)


@api.dispatcher.add_class
class Users:
    def me(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return request.user
        return {'error': '401', 'message': 'Not authenticated'}


@api.dispatcher.add_class
class Books:
    def list(self, request, *args, **kwargs):
        return BookSerializer(Book.objects.all(), many=True).data

    def retrieve(self, request, pk):
        obj = Book.objects.filter(pk=pk).first()
        if obj is None:
            return {"error": 404, "message": "Not Found"}
        return BookSerializer(obj).data

    def create(self, request: HttpRequest, book):
        serializer = BookSerializer(data=book)
        if not serializer.is_valid():
            return {"error": 400, "message": serializer.errors}
        book = Book(**book)
        book.save()
        return BookSerializer(book).data

    def update(self, request: HttpRequest, book):
        serializer = BookSerializer(data=book)
        if not serializer.is_valid():
            return {"error": 400, "message": serializer.errors}
        if 'pk' not in book:
            return {"error": 400, "message": "pk field required"}
        obj = Book.objects.filter(pk=book['pk']).first()
        if obj is None:
            return {"error": 404, "message": "Not Found"}
        for k, v in book.items():
            obj.__setattr__(k, v)
        obj.save()
        return BookSerializer(obj).data

    def delete(self, request, pk):
        obj = Book.objects.filter(pk=pk).first()
        if obj is None:
            return {"error": 404, "message": "Not Found"}
        obj.delete()
        return {}
