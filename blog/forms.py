from django import forms
from .models import Post
from django.forms import ModelForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image',)

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')



'''
form은 입력양식을 다루는 기능이다. 반복되는 처리를 장고가 대신하고 이용자는 데이터(model)와 표현물(template)에만 집중할수 있게된다
관리자 기능을 넘어서 조금더 많은 기능을 가진 것을 이용함
form으로 강력한 인터페이스를 만들수 있음. ModelForm을 생성해 자동으로 모델에 결과물을 저장함
클라이언트로부터 전송받은 데이터가 유효한지 검사하고 걸러내는 역할을 장고폼이 함. (ex. EmailField를 이용할시, .wiki나, .google과 같은 새로운 최상위 도메인, 심지어 IPv4나 IPv6과 같이 ip주소로 구성된 전자우편 주소에 대응 가능)

forms model을 import를 하고 (from django import forms), 그다음으로 Post model도 import함 (from .models import Post)
PostForm은 우리가 만든 폼의 이름임. 장고에 이 폼이 ModelForm이라는 것을 알려줘야함
그러므로 forms.ModelForm을 입력하여 ModelForm이라는 것을 알려주는 구문임을 알수있다.

class Meta: 이 구문은 이 폼을 만들기 위해서 어떤 model이 쓰여야 하는지 장고에 알려주는 구문 (model=Post)
이 폼에 필드를 넣으면 완성이 됨. title, text가 보여짐.
author는 현재 로그인한 유저인것을 확인

모델 폼 이용을 함. 모델의 속성을 그대로 가져올수 있기때문에 코드가 간단해짐.

ImageField 폼필드는 클라이언트가 제출한 파일이 이미지 파일인지 확인하는 방법은 대표적으로 verify()에 의존함
그마저도 일부파일에 대해서만 제공하여 GIF파일을 처리하는 모둘엔 verify()가 아예없음.
이미지 파일은 일반 문자열을 담는 Metadate 영역(chunk)을 지원하는데, 이요소를 악용하여 보안을 위협하는 코드를 삽입하여 해를 끼칠 가능성이 있음.

'''
