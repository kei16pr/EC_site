# Generated by Django 3.0.6 on 2020-06-09 20:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,null=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='タグ名')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('thumbnail', models.ImageField(default='/no_img.jpg', upload_to='documents/', verbose_name='サムネ')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='作成日')),
                ('detail', models.TextField(blank=True, max_length=255, null=True, verbose_name='詳細文')),
                ('ref', models.URLField(max_length=255, verbose_name='外部リンク')),
                ('tags', models.ManyToManyField(blank=True, null=True, to='main.Tag', verbose_name='タグ')),
            ],
        ),
    ]
