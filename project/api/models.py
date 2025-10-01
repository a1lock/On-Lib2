from django.db import models
from django.contrib.auth.models import User

# Модель "Книга"
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=100, verbose_name="Автор")
    description = models.TextField(verbose_name="Описание")
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name="Обложка")

    def __str__(self):
        return f'"{self.title}" - {self.author}'

# Модель "Отзыв"
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'Отзыв от {self.user.username} на книгу "{self.book.title}"'