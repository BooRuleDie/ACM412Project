from django.contrib import admin
from .models import Users, Topics, Comments, Upvotes, Downvotes

admin.site.register(Users)
admin.site.register(Topics)
admin.site.register(Comments)
admin.site.register(Upvotes)
admin.site.register(Downvotes)
