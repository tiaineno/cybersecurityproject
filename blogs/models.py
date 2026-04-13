from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

class LoginLog(models.Model):
	username = models.CharField(max_length=150)
	success = models.BooleanField()
	timestamp = models.DateTimeField(auto_now_add=True)
	ip_address = models.CharField(max_length=45, null=True, blank=True)

	def __str__(self):
		status = "Success" if self.success else "Failed"
		return f"{self.username} - {status} - {self.timestamp}"
