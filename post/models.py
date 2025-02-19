from django.db import models

class Post(models.Model):
    class SentimentChoice(models.TextChoices):
        positive = 'positive'
        negative = 'negative'
    title = models.CharField(max_length = 100)
    post = models.TextField()
    sentiment = models.CharField(choices=SentimentChoice.choices, blank=True)
    added_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'sentiment: {self.sentiment}, post: {self.title}'