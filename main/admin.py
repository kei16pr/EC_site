from django.contrib import admin
from .models import Post, Tag
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class PostResource(resources.ModelResource):
    class Meta:
        model = Post
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('title', 'thumbnail' ,'tags','detail','ref')
        exclude = ('created_at', 'id',)

class PostAdmin(ImportExportModelAdmin):
    resource_class = PostResource

admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
