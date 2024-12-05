from django import forms 
from .models import Comment
class CommentForm(forms.ModelForm): 
    class Meta: 
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add your comment here...'})
        }