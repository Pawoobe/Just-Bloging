from django.conf.urls import url #User 모델을 불러옴 // 현재는 슈퍼유저밖에없으니, 슈퍼유저 등록했던 사용자 출력
from . import views
from blog.views import *

urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^search/$', SearchFormView.as_view(), name='search'),
    url(r'^create/$', views.create, name='create'),
]

'''
장고의 메소드와 blog 애플리케이션에서 사용한 모든 views를 불러오고 있음

*url(r'^$', views,post_list, name='post_list'), : post_list라는 이름의 view가 ^$ url에 할당된 상태
^에서 시작해$로 끝난다는것은 문자열이 아무것도 없는 상태를 의미함. 결국 누군가 웹사이트에 처음들어왓을때 가장 먼저
views.post_list를 보여주는것

*url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'), : post_list 내용에 추가된 부분
post/ : URL이 post문자를 포함해야 하는다는것을 의미, (?P<pk>\d+):pk변수에 모든 값을 넣어 뷰로 전송하겠다는 의미
\d: 문자를 제외한 숫자 0부터 9중, 한가지 숫자만 볼수있음. +:하나 또는 그 이상의 숫자가 올수있음.
ex)0.0.0.0:8000/post/ 라고 적었을땐, 해당사항이 아니나, 0.0.0.0:8000/post/12344235/라고는 적었을땐, 정확하게 매칭이뙨다
글을 쓸때마다 1씩 증가되므로 첫번째 게시물은 post/1이 된다.
/: 다음에 /가 한번 더와야하는 의미, $:마지막 부분
ex)0.0.0.0:8000/post/5 라고 입력할시, 장고는 post_detail 뷰를 찾아 매개변수가 pk가 5인 값을 찾아 뷰로 전달한다.
pk는 원하는 변수명, 원하는 이름으로 변경할수 있음 pk를 post_id로 바꾸면 정규표현식도 (?P<post_id>\d+)로 변경이 된다.

*url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'), : pk변수에 모든 값을 넣어 뷰로 전송,

*url(r'^drafts/$', views.post_draft_list, name='post_draft_list'), : 수정 버튼 url


'''
