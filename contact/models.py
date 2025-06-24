from django.db import models

class Review(models.Model):
    """
    Model to store contact information.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Review {self.name} <{self.email}>"
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"