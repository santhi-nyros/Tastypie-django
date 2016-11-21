from django.contrib import admin
from api.models import Entry,Recipe,UserProfile,Post
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(UserProfileAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        user = request.user
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
        return super(UserProfileAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )











admin.site.register(Entry)
admin.site.register(Recipe)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Post)
