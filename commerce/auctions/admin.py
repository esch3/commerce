from django.contrib import admin
from .models import User, AuctionListing, Bid, Comment

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id", 
        "title", 
        "description", 
        "photo", 
        "price", 
        "date",
        "category"
    )

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)