from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm
from .models import Post #현재디렉토리 애플리케이션에서

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # 현재 model.py의 Post 클래스의 객체를 필터링해서 정렬한뒤. posts라는 쿼리셋을 불러온다.
    return render(request, 'blog/post_list.html', {'posts': posts})
    # render를 통해 매개변수로 받은 사용자의 request를 html템플릿으로 변수를 보내준다.

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
    if request.method == "POST":
        form =PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
            # 위에 보이는 post_detail 함수를 통해서 함수 detail한 부분을 보여주는 곳으로 이동 시킨다. 라는 뜻이다.
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form':form})
        # post_edit.html에서 form이라고 키값을 입력해주면 form=PostForm()이렇게해서 받은 객체를 꺼내서 쓸수가있다.

# post_new랑의 차이점이 pk 매개변수를 따로 받고있다.
def post_edit(request, pk):
    # pk 매개변수를 받아서 , 수정하고자 하는 글의 post 모델 인스턴스를 가져온다. (pk를 이용해서)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post) # post 폼을 만들고 그 폼안에 데이터를 post 객체 데이터로 넣는다.
        if form.is_valid():  # 폼이 유효하면
            post = form.save(commit=False) #폼을 바로 저장하지말고 (commit=False)가 바로 저장 X
            post.author = request.user # user 이름을 author로
            post.published_date = timezone.now()  # published_date는 현재 시각으로 바꾸고
            post.save()         #저장한다.
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})
