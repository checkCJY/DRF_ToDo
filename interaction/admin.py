from django.contrib import admin
from .models import TodoLike, TodoBookmark, TodoComment

admin.site.register(TodoLike)
admin.site.register(TodoBookmark)
admin.site.register(TodoComment)
