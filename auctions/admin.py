from django.contrib import admin
from .models import User, Listing, Bid, Comment, Watchlist

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username", "email")
    list_filter = ("username", "email")

class BidInline(admin.TabularInline):
    model = Bid
    extra = 1  # Number of empty forms to display

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "category", "starting_bid", "current_bid", "bid_count", "date", "active")
    search_fields = ("title", "description", "user__username", "category")
    list_filter = ("category", "active", "date")
    inlines = [BidInline, CommentInline]  # Adds inline editing for bids and comments

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "amount")
    search_fields = ("user__username", "listing__title")
    list_filter = ("listing", "user")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "text", "date")
    search_fields = ("user__username", "listing__title", "text")
    list_filter = ("date",)

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "display_listings")
    search_fields = ("user__username", "listings__title")
    list_filter = ("listings",)

    def display_listings(self, obj):
        # Return a comma-separated list of listing titles
        return ", ".join(listing.title for listing in obj.listings.all())
    display_listings.short_description = 'Listings'  # Optional: Add a custom header for this column
    
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)

