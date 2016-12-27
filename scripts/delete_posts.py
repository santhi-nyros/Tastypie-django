# scripts/delete_all_questions.py
from datetime import timedelta

from django.utils import timezone

from api.models import Comment,Post

def run(*args):
	print list(args)
	if list(args):
		comments = Comment.objects.filter(id__in=list(args))
		print comments
		comments.delete()
	else:
		print "empty list given."


