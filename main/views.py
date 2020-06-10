from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Post, Tag
from django.urls import reverse_lazy
from .forms import CSVUploadForm
import csv
import io
import urllib
from django.http import HttpResponse
from itertools import chain

def index(request):
    return render(request,'main/page.html')

class IndexView(generic.ListView):
    model = Post
    paginate_by = 20

    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)|Q(text__icontains=keyword)
            )
        return queryset


class CategoryView(generic.ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs['pk'])
        queryset = Post.objects.order_by('-created_at').filter(tags=tag)
        return queryset


class DetailView(generic.DetailView):
    model = Post

class PostImport(generic.FormView):
    """テーブルの登録(csvアップロード)"""
    template_name = 'main/import.html'
    success_url = reverse_lazy('main:index')
    form_class = CSVUploadForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_name'] = 'main'
        return ctx

    def form_valid(self, form):
        """postされたCSVファイルを読み込み、役職テーブルに登録"""
        csvfile = io.TextIOWrapper(form.cleaned_data['file'])
        reader = csv.reader(csvfile)
        for row in reader:
            """
            テーブルをコード(primary key)で検索
            """
            post, created = Post.objects.get_or_create(pk=row[0])
            post.title = row[1]
            post.thumbnail = row[2]
            post.detail = row[4]
            post.ref = row[5]
            post.save()
            tags = row[3]
            tags = tags.replace("['","").replace("']","").replace(" ","")
            tags = tags.split("','")
            # tags=tags.replace("[<Tag: ","").replace(">]","")
            # tags=tags.split(">, <Tag: ")
            for tag in tags:
                try:
                    tag = Tag.objects.get(name=tag)
                    post.tags.add(tag)
                except:
                    new_tag = Tag(name=tag)
                    new_tag.save()
        return super().form_valid(form)


def PostExport(request):
    """
    役職テーブルを全件検索して、CSVファイルを作成してresponseに出力します。
    """
    response = HttpResponse(content_type='text/csv;')
    filename = urllib.parse.quote((u'Postデータ.csv').encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
    writer = csv.writer(response)
    for post in Post.objects.all():
        writer.writerow([post.pk, post.title,post.thumbnail,[tag for tag in post.tags.all()],post.detail,post.ref])
    return response
