from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Genre, Author, Feedback, Interaction, Book 
from .serializers import *
import rest_framework.status as status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db.models import Avg

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
    'http://127.0.0.1:8000/api/books/',
    'http://127.0.0.1:8000/api/genres/',
    'http://127.0.0.1:8000/api/authors/',
    'http://127.0.0.1:8000/api/interactions/',
    'http://127.0.0.1:8000/api/interactions/book/',
    'http://127.0.0.1:8000/api/feedbacks/',
]
    return Response(routes)

from base.products import products

@api_view(['GET'])
def search(request):
    print("Request:", request)
    query = request.query_params.get('query', '')
    print("Received query:", query)

    # Search for books based on title, author, or genre
    books_by_title = Book.objects.filter(title__icontains=query)
    books_by_author = Book.objects.filter(author__name__icontains=query)
    books_by_genre = Book.objects.filter(genre__name__icontains=query)
    
    # Combine the querysets and remove duplicates
    books = (books_by_title | books_by_author | books_by_genre).distinct()
    
    # Serialize the results
    books_serializer = BookSerializer(books, many=True)

    serializer = BookSerializer(books, many=True)
    return Response({
        'books': books_serializer.data,
    })


@api_view(['GET', 'POST'])
def getBooks(request):
    if request.method == 'GET':
        books = Book.objects.annotate(mean_rating=Avg('rating__rating'))
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getBook(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, many=False)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({'detail': 'Book does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Book ID'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
def updateBook(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Book.DoesNotExist:
        return Response({'detail': 'Book does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Book ID'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteBook(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response({'detail': 'Book deleted successfully'})
    except Book.DoesNotExist:
        return Response({'detail': 'Book does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Book ID'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def getGenre(request, pk):
    try:
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre, many=False)
        return Response(serializer.data)
    except Genre.DoesNotExist:
        return Response({'detail': 'Genre does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Genre ID'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def getGenres(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def updateGenre(request, pk):
    try:
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(instance=genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Genre.DoesNotExist:
        return Response({'detail': 'Genre does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Genre ID'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def deleteGenre(request, pk):
    try:
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response({'detail': 'Genre deleted successfully'})
    except Genre.DoesNotExist:
        return Response({'detail': 'Genre does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Genre ID'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def getAuthors(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def getAuthor(request, pk):
    try:
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)
    except Author.DoesNotExist:
        return Response({'detail': 'Author does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Author ID'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updateAuthor(request, pk):
    try:
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(instance=author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Author.DoesNotExist:
        return Response({'detail': 'Author does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Author ID'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def deleteAuthor(request, pk):
    try:
        author = Author.objects.get(pk=pk)
        author.delete()
        return Response({'detail': 'Author deleted successfully'})
    except Author.DoesNotExist:
        return Response({'detail': 'Author does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Author ID'}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET', 'POST'])
def getFeedbacks(request):
    if request.method == 'GET':
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def deleteFeedback(request, pk):
    try:
        feedback = Feedback.objects.get(pk=pk)
        feedback.delete()
        return Response({'detail': 'Feedback deleted successfully'})
    except Feedback.DoesNotExist:
        return Response({'detail': 'Feedback does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Feedback ID'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def getInteractions(request):
    if request.method == 'GET':
        interactions = Interaction.objects.all()
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = InteractionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def getInteraction(request, pk):
    try:
        interaction = Interaction.objects.get(pk=pk)
        serializer = InteractionSerializer(interaction, many=False)
        return Response(serializer.data)
    except Interaction.DoesNotExist:
        return Response({'detail': 'Interaction does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Interaction ID'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def getInteractionsByBook(request, book_id):
    try:
        interactions = Interaction.objects.filter(book_id=book_id)
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)
    except ValueError:
        return Response({'detail': 'Invalid Book ID'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def updateInteraction(request, pk):
    try:
        interaction = Interaction.objects.get(pk=pk)
        serializer = InteractionSerializer(instance=interaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Interaction.DoesNotExist:
        return Response({'detail': 'Interaction does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Interaction ID'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteInteraction(request, pk):
    try:
        interaction = Interaction.objects.get(pk=pk)
        interaction.delete()
        return Response({'detail': 'Interaction deleted successfully'})
    except Interaction.DoesNotExist:
        return Response({'detail': 'Interaction does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'detail': 'Invalid Interaction ID'}, status=status.HTTP_400_BAD_REQUEST)

    
class RatingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer
    
    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)
    
    # Other viewset methods...
    
    def get_rating_id_by_user_and_book(self, request, user_id, book_id):
        print(request)
        # Retrieve the rating based on user_id and book_id
        rating = get_object_or_404(Rating, user_id=user_id, book_id=book_id)

        # Extract the rating ID
        rating_id = rating.id

        # Return the rating ID as JSON response
        return JsonResponse({'rating_id': rating_id})
    def get_rating_by_user_and_book(request, user_id, book_id):
        # Retrieve the rating based on user_id and book_id
        rating = get_object_or_404(Rating, user_id=user_id, book_id=book_id)

        # Extract the rating value
        rating_value = rating.rating  # Assuming 'rating' is the field containing the rating value

        # Return the rating value as JSON response
        return JsonResponse({'rating': rating_value})

        
class ListRatingViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class CreateRatingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Request Data:", request.data)
        existing_rating = Rating.objects.filter(user=request.user, book_id=request.data.get('book'))
        if existing_rating.exists():
            return Response({'detail': 'You have already rated this book'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response({'detail': 'Rating created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveRatingViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Rating.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        rating_id = self.kwargs.get('pk')
        if rating_id:
            queryset = queryset.filter(id=rating_id)
        else:
            queryset = queryset.none()
        return queryset

    # Set the serializer_class attribute to use the custom serializer
    serializer_class = RatingWithoutIdSerializer

class UpdateRatingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer  # Define your serializer class here

    def get_queryset(self):
        # Customize queryset based on your requirements
        return Rating.objects.filter(user=self.request.user) 
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'You are not allowed to update this rating'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RatingSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class DestroyRatingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer  # Define your serializer class here

    def get_queryset(self):
        # Customize queryset based on your requirements
        return Rating.objects.filter(user=self.request.user) 
        
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.user != request.user:
                raise PermissionDenied("You are not allowed to delete this rating")
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Rating.DoesNotExist:
            raise NotFound("Rating not found")
    
@api_view(['GET'])
def get_ratings_for_book(request, book_id):
    try:
        # Your view logic here
        ratings = Rating.objects.filter(book_id=book_id)
        num_reviews = ratings.count()
        total_rating = sum(rating.rating for rating in ratings)
        average_rating = total_rating / num_reviews if num_reviews > 0 else 0

        data = {
            'average_rating': average_rating,
            'num_reviews': num_reviews
        }
        return Response(data)
    except ValueError:
        return Response({'detail': 'Invalid Book ID'}, status=status.HTTP_400_BAD_REQUEST)


    