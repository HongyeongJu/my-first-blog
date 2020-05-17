from django.shortcuts import render
from django.utils import timezone
from .models import Post #현재디렉토리 애플리케이션에서

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # 현재 model.py의 Post 클래스의 객체를 필터링해서 정렬한뒤. posts라는 쿼리셋을 불러온다.
    return render(request, 'blog/post_list.html', {'posts': posts})
    # render를 통해 매개변수로 받은 사용자의 request를 html템플릿으로 변수를 보내준다.
