from django import forms
from .models import Keyword

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ['name']
        labels = {'name': '키워드:'}    # 'name' 필드의 레이블을 '키워드:'로 설정
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 200px;'}) 
        }