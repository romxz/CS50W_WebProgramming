from django.contrib.auth.models import User

user = User.objects.create_user("alice", "alice@something.com", "alice13370")

user.first_name = "Alice"
user.save()
