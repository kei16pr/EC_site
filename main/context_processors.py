from .models import Tag


def common(request):
    """テンプレートに毎回渡すデータ"""
    context = {
      'category_list':Tag.objects.all(),
    }
    return context
