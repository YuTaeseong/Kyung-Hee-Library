from django.contrib import admin
from .models import library_profile, user_barrow_books, user_token

# Register your models here.
admin.site.register(library_profile)
admin.site.register(user_barrow_books)
admin.site.register(user_token)