from django.conf.urls import include, url #User 목록을 불러움
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from blog.views import detail
from blog.views import create

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls')),
    url(r'^blog/(?P<pk>[0-9]+)$',detail, name='detail'),
    url(r'^blog/upload/$', create, name='create'),
    url(r'^accounts/login/', auth_views.login, name='login', kwargs={'template_name': 'login.html'}),
    url(r'^accounts/logout/', auth_views.logout, name='logout', kwargs={'next_page': settings.LOGIN_URL}),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''
현재 admin안의 내용, static내용과 settings의 내용을 가져옴
장고는 admin/ 로 시작하는 모든 url을 view와 대조해 찾아냄 무수히 많은 URL이 admin URL에 포함될 수 있어 일일히 다쓸수없음
정규 표현식 이용
/// 장고2.0 버전부터는 정규이용식 필요없음
*정규표현식
^post/(\d+)/$
^post/: url이 오른쪽부터 post/로 시작, (\id+):숫자 한개이상있음, /: /뒤에 문자가있음. $:url마지막이 /로 끝남

*url(r'', include('blog.urls')), : 메인 url로 blog.urls를 가져옴

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static파일과는 다르게 개발서버에 기본서빙 미지원한다
개발 편의성 목적으로 서빙 rule 추가 기능
settings.DEBUG=False 일때는 static 함수에서 빈 리스트 리턴

url(r'^blog/(?P<pk>[0-9]+)$',
    detail, name='detail')
    + : 앞에 지정한 문자열 패턴이 한번 이상 반복. 웹브라우저에서 사진하나의 내용을 볼땐 /blog/<사진 ID>/ 를 통해서보게 되는데, 이중에서 [0-9]만 작성할시 0에서 9까지의 숫자밖에 안나오기 때문이다. 3자리 수든, 4자리수든 +하나만 넣으면 된다.
    숫자D가 아닌 영소문자로 구성되어있을시, [a-z]+로 작성하면 된다

    업로드된 파일은 upload_files이라는  url르 따르므로 urls.py에도 관련된 내용을 등록해야한다. upload_files 뒤에 나오는 경로를 받은 뒤 지정된 경로에 있는 이미지 파일을 읽어온 후 웹 브라우저에 보내는 것이다 (경로가 없으면 404 오류)
    이러한 과정을 금방 처리해주는 기능이 from django.conf.urls.static import static 모듈의 static함수.

r'^accounts/login/' : 은 로그인하는 URL임, 로그인 화면을 출력하거나, 로그인 인증처리를 하는 뷰 함수는 Django에 내장, login뷰 함수를 이용
r'^accounts/logout/' : 로그아웃 하는 URL 로그인 기능과 마찬가지. 키워드 인자 next_page 는 로그아웃 하고 난 뒤에 이동할 URL을 의미함. template_name 을 지정하지 않으면, django에 내장된 로그아웃 화면이 나옴.
from django.contrib.auth import views as auth_views 모듈 안에 함수 객체가 존재함. kwargs는 URL패턴에 연결한 뷰함수에 추가로 전달할 인자를 사전형객체로 전달함 ==> login.html로 전송

'''
