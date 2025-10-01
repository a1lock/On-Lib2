from django.contrib.auth.models import User
from .models import Book
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .serializers import UserSerializer, BookSerializer
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm

# 1. API для регистрации и авторизации (Ответственный: Никита)
# ---

# Эндпоинт для регистрации нового пользователя (POST /api/register)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,) # Разрешить всем доступ к регистрации
    serializer_class = UserSerializer

# Эндпоинт для аутентификации и выдачи токена (POST /api/login)
# Мы используем встроенное представление из simple-jwt
class LoginView(TokenObtainPairView):
    pass


# 2. API для работы с книгами (Ответственный: Дмитрий)
# ---

# Эндпоинт для получения списка книг и поиска (GET /api/books и GET /api/books/search?q=...)
class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = Book.objects.all()
        # Проверяем, есть ли параметр 'q' в запросе для поиска
        query = self.request.query_params.get('q', None)
        if query is not None:
            # Фильтруем по названию или автору без учета регистра
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        return queryset

# Эндпоинт для получения детальной информации по ID книги (GET /api/books/{id})
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.AllowAny,)


# 3. API для управления библиотекой (Ответственный: Никита)
# ---
# Используем ViewSet для объединения логики CRUD (Create, Retrieve, Update, Destroy)

from rest_framework import viewsets

# Эндпоинты для администратора:
# GET /api/admin/books - список книг
# POST /api/admin/books - добавление книги
# PUT /api/admin/books/{id} - редактирование книги
# DELETE /api/admin/books/{id} - удаление книги
class BookAdminViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Требуются права администратора для доступа
    permission_classes = [permissions.IsAdminUser]

def index_page(request):
    # Получаем 4 последние добавленные книги для демонстрации
    latest_books = Book.objects.order_by('-id')[:6]
    # Передаем их в шаблон
    context = {'latest_books': latest_books}
    return render(request, 'index.html', context)

def catalog_page(request):
    # Получаем параметр 'q' из GET-запроса (из адресной строки)
    search_query = request.GET.get('q', '')

    if search_query:
        # Если есть поисковый запрос, фильтруем книги
        books = Book.objects.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )
    else:
        # Если запроса нет, показываем все книги
        books = Book.objects.all()

    context = {'books': books, 'search_query': search_query}
    return render(request, 'catalog.html', context)

def book_detail_page(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.order_by('-created_at')
    form = ReviewForm() # Создаем пустой экземпляр формы

    # --- НАЧАЛО НОВОЙ ЛОГИКИ ДЛЯ ОБРАБОТКИ ФОРМЫ ---
    if request.method == 'POST':
        # Проверяем, что пользователь залогинен, прежде чем что-то делать
        if request.user.is_authenticated:
            form = ReviewForm(request.POST) # Заполняем форму данными из запроса
            if form.is_valid():
                # form.save(commit=False) создает объект, но не сохраняет его в БД
                new_review = form.save(commit=False)
                # Присваиваем книге и пользователю нужные значения
                new_review.book = book
                new_review.user = request.user
                # А теперь сохраняем в базу данных
                new_review.save()
                # Перенаправляем пользователя на ту же страницу, чтобы избежать
                # повторной отправки формы при перезагрузке
                return redirect('book_detail', book_id=book.id)
    # --- КОНЕЦ НОВОЙ ЛОГИКИ ---

    context = {
        'book': book,
        'reviews': reviews,
        'form': form, # <-- Добавляем форму в контекст
    }
    return render(request, 'book_detail.html', context)

def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} был создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile_page(request):
    # Контекст передавать не нужно, так как объект user доступен во всех шаблонах
    return render(request, 'profile.html')