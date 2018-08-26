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


'''
views.py : 특정주소에 접근화면에 내용을 표시하는 파이썬 함수를 호출하는 내용을 담는 부분
우리가 인지하는 표현물로 안내하는 역할 (ex. 프린터)
django내에서는 template가 표현물로 확인.
데이터를 표현하는 연결자이자 안내자.

views파일은 모델과 템플릿을 연결하는 역할 ex.post_list를 뷰에서 보여주고 이를 템플릿을 전달하기 위해 모델을 가져와야함.
일반적으로 view가 템플릿에서 모델을 선택하도록 만들어야함.
*def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

post_list라는 함수(def)를 만들어 요청(request)을 넘겨받아 render 메소드를 호출함
이 함수는 호출하여 받은(return) blog/post_list.html template을 보여줌

*def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    글 목록을 게시일 published_date 기준으로 정렬함.
    return render(request, 'blog/post_list.html', {'posts': posts})
render함수에는 매개변수 request (사용자가 요청하는 모든것)와 'blog/post_list' 템플릿이 존재함
"{}" 안에 템플릿을 사용하기 위해 매개변수를 추가함. (매개변수 이름: 'posts')
":" 이전에 문자열이 와야하고. ''를 양쪽에 붙여야함


*def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
폼을 제출할때, 같은뷰를 불러온다. 이때 request에는 우리가 입력한 데이터들을 가지고있는데 request.POST가 이 데이터를 가지고있음.
(POST는 글 데이터를 "등록하는 (posting)하는 것을 의미함" 블로그 "글"을 의미하는 "post" 관련없음.) <form>정의에 method="POST"라는 속성이 있었는데
이렇게 POST로 넘겨진 폼 필드의 값들은 이제 request.POST에 저장이 된다. POST로 저장이 된 값을 다른것으로 바꾸면 안됨

if request.method == "POST":
    [...]
else:
    form = PostForm()
접속자가 새 글을 쓸수 있게 안의 폼은 비어있어야함.
폼에 입력된 데이터를 view페이지로 가져올때, 조건문을 추가시킴.
method가 POST라면 폼에서 받은 데이터를 PostForm으로 넘겨야 하므로 form = PostForm(request.POST)으로 작성
이 후에는 폼에있는 값들이 올바른지 확인해야함 (모든 필드에 값이 있으며, 잘못된 값이 있을때 저장되지않아야함.)

*if form.is_valid():
    post = form.save(commit=False)
    post.author = request.user
    post.published_date = timezone.now()
    post.save()

form.save()로 폼을 저장하는 작업과 동시에 작성자를 추가하는 작업이 있음 (PostForm에는 작성자(author)) 필드가 없으나, 필드값이 필요함
commit=False란 넘겨진 데이터는 바로 Post 모델에 저장하지않음을 의미함. 작성자를 추가한 다음 저장해야함.
post.save()는 변경사항(작성자 정보 포함)을 유지할 것이고 새 블로그 글이 만들어짐
작성 한뒤, post_detail 페이지로 이동하기 위해
from django.shortcuts import redirect을 추가함.
추가적으로, post_detail뷰는 pk변수가 필요함으로 pk=post.pk를 사용해서 뷰에게 값을 넘겨줌
*return redirect('post_detail', pk=post.pk) post는 새로 생성한 블로그 글임.

*def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)

url로부터 추가로 pk 매개변수를 받아서 처리한뒤,
get_object_or_404(Post, pk=pk)를 호출하여 수정하고자 하는 글의 Post 모델 instance로 가져옴. (pk로 원하는 글을 찾음)
이렇게 가져온 데이터를 폼을 만들때와, 글 수정할때 이전에 입력했던 데이터를 가지고 폼을 저장할때 사용.
함
*def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})
(published_date__isnull=True) 코드로 발행되지 않은 글 목록을 가져옴. (order_by('created_date')) 코드로 created_date필드에 대해
오름차순 정렬을 수행함.


이미지 관련
form = ImageForm(request.POST, request.FILES)을 통해 ImageForm을 요청받을때 사용할 폼으로 설정
POST로 날아온 요청에 대하여 코드를 수행 / 사용자가 upload버튼을 눌렀을때 동작하는 부분
form.is.valid()를 통해 맞지않는 형식의 파일을 걸러냄
리턴값에 'form' : form을 템플릿에 추가적으로 넘겨주어야 템플릿에서 form형태로 사용가능함
모델에서 작성했던 (동적 경로를 지정해주는 함수) generate_upload_path 호출

이용자가 뭔가를 요청하면 그 url에 대한 정보를 urls.py로 대표되는 것을 찾아서 실행한다.
**이 과정에서 데이터(Model)을 가져와 출력을 바로 하기도하고 // template을 거쳐서 출력문을 만들어서 출력하기도 한다.
이과정의 연결부분 역할을 views가 하는것이다.

deatil함수로 pk나느 인자를 넘기는 과정을 거쳐서 이미지가 올라간다. pk는 urls.py에서 (?P<pk>[0-9]+) 부누이다.
정규표현식 패턴에 해당되는 문자열이 ?P<이름>에 지정된 이름에 저장되어 view함수의 인자로 넘겨진다.
/blog/숫자/ url에서 숫자가 pk라는 이름을 갖는 인자에 저장되어 detail view 함수로 전달된다. 그래서 deatil함수가 이 인자를 받도록해야한다

먼저 from .models import Photo문으로 blog앱에 있는 models 모듈에서 Photo모델을 가져옴 (.models는 photo.models타은 내용이며, views.py 파일과 같은 디렉토리에 있기때문이다.)
그다음에 Photo모델의 objects객체의 get 메소드를 이용해 뷰 함수의 인자 pk에 해당하는 사진 데이터 (Photo모델의 객체(instance))를 가져와서 photo라는 변수에 담는다.
Photo 모델에 있는 image라는 필드에 접근해서 url속성을 이용해 지정한 사진의 URL을 출력함

*        try:
            photo = Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            return HttpResponse("사진이 없습니다")
DoesNotExist라는 예외상황이 발생하면, try/except문으로 잡아내서 예외처리를 하는것임.
그런데 Photo모델로 사진 데이터를 가져오려는데 데이터가 없는 상황은 "없는 페이지로 확인됌." 이런상황에서는 404오류를 일으키니, 오류안내 페이지를 따로 만들어 제공을 해야함
from django.shortcuts import get_object_or_404

form = PhotoForm(request.POST, request.FILES)의 내용 PhotoForm폼에 첫번째 인자로 request.POST를 두번째 인자로 request.FILES를 전달함. 첫번째 인자는 폼에서 다룰 데이터를 뜻함
사전형 객체나, 사전형 객체처름 동작하는 객체여야함. 파일을 제외한 HTML Form에서 POST방식으로 전송해온 모든 formdata데이터가 request.POST에 있다. 파일은 request.FILES에 있음.
'''
