from django.contrib import admin

from reviews.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role', 'bio',)
    list_display_links = ('pk', 'username',)
    list_editable = ('role',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'


admin.site.site_header = 'YaMDb'
admin.site.site_title = 'YaMDb'
