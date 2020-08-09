from django.contrib import admin

from .models import User, Listing, Comment, Category, CurrentBid, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(CurrentBid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist)