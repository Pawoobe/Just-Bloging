from django.shortcuts import render
from django.utils import timezone #timezone의 모듈을 불러옴
from .models import Post #models.py 파일에 정의된 모델을 가져옴 / "."은 현재 디렉토리 또는 어플리케이션을 의미함. 동일한 디렉토리 내에 views . models 파일이 있기때문에 ". 파일명"으로 내용을 가져올수 있음
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404 #장고에서 주어진 기능. pk에 해당하는 Post가 없을경우, 404페이지를 보여줌
from .forms import PostForm
from django.views.generic.edit import FormView # FormView 클래스형 제네릭 뷰를 import
from blog.forms import PostSearchForm
from django.db.models import Q # 검색기능에 필요한 q 클래스를 import
from django.http import HttpResponse
from django.views import generic

class PostListView(generic.ListView):
    model = Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "GET":
        form = PostForm(request.POST)
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            obj = form.save()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


class SearchFormView(FormView):
    # form_class를 forms.py에서 정의했던 PostSearchForm으로 정의
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    # 제출된 값이 유효성검사를 통과하면 form_valid 메소드 실행
    # 여기선 제출된 search_word가 PostSearchForm에서 정의한대로 Char인지 검사
    def form_valid(self, form):
        # 제출된 값은 POST로 전달됨
        # 사용자가 입력한 검색 단어를 변수에 저장
        search_word = self.request.POST['search_word']
        # Post의 객체중 제목이나 설명이나 내용에 해당 단어가 대소문자관계없이(icontains) 속해있는 객체를 필터링
        post_list = Post.objects.filter(Q(title__icontains=search_word) |
                                        Q(text__icontains=search_word)
                                        )

        context = {}
        # context에 form객체, 즉 PostSearchForm객체 저장
        context['form'] = form
        context['search_term'] = search_word
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)

