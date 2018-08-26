from __future__ import unicode_literals
from django.db import models #db package의 models 모듈에있는 Model클래스를 사용하여 만들기 때문에 이용
from django.utils import timezone
from django.urls import reverse_lazy
'''
from 또는 import로 시작하는 부분은 다른 파일에 있는것을 추가하라는 의미. 복사 & 붙혀넣기와 같은 기능
Imagefield 는 FileField와 거의 동일하며, 차이점은 이미지의 가로 세로 길이를 정할 수있음
imagekit (Pillow라이브러리 이용)는 이미지의 변화가 생길수 있는 모델  == 설치필요

'''
class Post(models.Model):   #모델을 정의하는 코드 (모델 = 객체)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    image = models.ImageField(upload_to='%Y/%m/%d/orig', blank=True, null=True) #원본 사진파일
    #create_at =  models.DateTimeField(auto_now_add=True)#생성일시

    class Meta:
        ordering = ['-id']

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Post, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        url = reverse_lazy('post_detail', kwargs={'pk': self.pk})
        return url

'''
models.py : 모델을 정의하는 모듈. 데이터를 구성하는 항목 자체(field)와 데이터를 다루는 행위를 포함
해당 정보를 오려내거나 복사하거나 날려보내는 것과 같이 관련행위로 구성.
사람이 인지할수 없는 단계
그저 데이터일뿐

*class Post(models.Model):
class : 객체를 정의한다는 것을 알려줌
Post : 모델의 이름 (이름이니까 다른 이름도 가능 / 항상 대문자로 시작)
models : Post가 장고 모델임을 의미함, Post가 데이터베이스에 저장되어야 한다고 인식식
*models.CharField : 글자수가 제한된 텍스트를 정의할때 사용 (ex. 글의 제목)
*models.TextField : 글자수가 제한이 없는 긴 텍스트를 위한 속성
*models.DateTimeField : 날짜와 시간을 의미함
*models.ForeignKey : 다른모델에 대한 링크를 의미함
*def publish(self): publish라는 이름을 가진 메소드 (변경가능)일


파일을 다루는 필드 FileField, 이런 필드 종류를 필드 타입이라 부름.
이 필드로 파일을 건네면 저장소 내에 파일을 저장하고 이 파일에 접근하는 연결자 역할을 하며, 파일 관련기능이나 정보를 제공함.
이미지 파일을 대상으로 하는 ImageField도 존재함. 실제로도 FileField를 상속받은 클래스. 이미지 면적, 길이 같은 정보를 제공하기 위해 ImageField를 사용하는것이 편함
필드 옵션 : upload_to, heigth_field, strong 등이 있음
id는 값이 겹치지 않는 색인, 각 사진을 구분짓는 고유값임.
DateTimeField : 생성일시 정보를 다룸. auto_now 옵션과, auto_now_add 옵션이 있고, True / False 로 구분 auto_now_add는 새로 생성될때, auto_now는 저장될때 자동으로 시간정보를 담음

null=True 는 None 자료형을 허용하겠다는 의미. 빈칸과 None은 전혀 다른의미임. 빈칸은 내용이 비어있는 문자형 객체임.
null=True 는 데이터베이스 테이블에 관한것. blank=True는 장고 폼에 대한 설정임.

upload_to/연/월/일/종류 로 구분

*args, **kwargs는 함수가 넘겨받는 인자를 미리 알지 못하는 경우에 인자를 담는 객체.
delete 메소드로 뭘 인자로 넘겨야할지 모르나, 넘겨받은 그대로 Model클래스의 delete메소드로 넘겨줘야 하기때문에 작성

self.image.delete() 에서 self.image는 image모델 필드를 뜻함
메소드 안에서 속성에 접근하려면 self.속성이름 으로 접근해야한다. 인스턴스 메소드에서 첫번째 인자로 delete를 받았고, 밖에서는 photo.image 이런식으로 접근이 필요.
image모델 필드는 ImageField클래스의 인스턴스임. ImageField클래스로 만든 인스턴스는 delete라는 인스턴스 메소드를 제공함
고로 self.filetered_image.delete()는 필터가 적용된 이미지 파일을 지우는것이다.
super(Photo, self).delete(*args, **kwargs)는 Photo모델이 상속받은 부모클래스의 delete 인스턴스 메소드를 호출함, 이 코드가 없을경우, 첨부된 업로드만 삭제되고 모델 객체를 사라지징낳음.
Model 클래스에 있는 delete메소드는 모델객체를 지우는것!!

'''
