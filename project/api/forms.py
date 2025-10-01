# api/forms.py

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # Говорим, что эта форма основана на модели Review
        fields = ['text']  # В форме будет только одно поле - для текста отзыва
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Ваш отзыв...',
                'rows': 4,
            }),
        }
        labels = {
            'text': '', # Убираем стандартную надпись "Text" над полем
        }