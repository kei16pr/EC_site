from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Post, Tag

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
