from django.db import models
from django.utils import timezone
class Tag(models.Model):
    """タグ"""
    name = models.CharField('タグ名',max_length=255)
    def __str__(self):
        return self.name

class Post(models.Model):
    """ブログの記事"""
    title = models.CharField('タイトル',max_length=255)
    thumbnail = models.ImageField('サムネ',upload_to='documents/', default='/no_img.jpg')
    created_at = models.DateTimeField('作成日',default=timezone.now)
    tags = models.ManyToManyField(Tag,verbose_name='タグ')
    detail = models.TextField('詳細文',max_length=255)
    ref = models.URLField('外部リンク',max_length=255)
    def __str__(self):
        return self.title
