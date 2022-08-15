from django.contrib import admin
from .models import Post, Comment, Images



#inlines
class ImagesInline(admin.TabularInline):
    model = Images

#ModelAdmin
class PostAdmin(admin.ModelAdmin):
    inlines = [ImagesInline]
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    readonly_fields = ("author",)
    
admin.site.register(Post, PostAdmin)


admin.site.register(Images)
admin.site.register(Comment)
