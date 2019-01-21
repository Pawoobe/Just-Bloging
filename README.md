# Just-Bloging

Django 설치후 django-admin.py 스크립트 실행

django

manage.py - 사이트 관리 스크립트 (별도의 설치없이 웹서버 이용가능)

mysite

        settings.py - 웹사이트 설정 파일
        
        urls.py - 웹사이트 URL 설정
        
        wsgi.py
        
        __init__.py
        

blog

        __init__.py
     
        admin.py -- django 관리자 스크립트 (수정 / 삭제 등등 가능)
     
        models.py - 모델선정 (원래 저장했던 함수 등을 다른 스크립트에서 호출가능)
     
        tests.py
     
        views.py - 로직에서 필요한 정보를 받아와 템플릿에 전달함
        
        apps.py
        
        forms.py - 모델폼을 생성해 자동으로 모델에 결과물을 저장가능

        urls.py - 새로 추가한 파일 / 웹사이트 URL 설정


   migrations  -- 마이그레이션 결과 
     
                __init__.py
     
                0001_initial.py
     
                0002_photo.py
     
                0003_auto_20180821_0406.py
        
   templates/blog - PYTHON 과 HTML 을 합쳐 제작한 동적 웹사이트
        
                base.html - 블로그의 기본 베이스 (이 파일을 이용해 다른파일에 적용시킴)
                
                post_detail.html - 글 확인 페이지
                
                post_draft_list.html - 글 수정 완료 페이지
                
                post_edit.html - 글 수정 페이지
                
                post_list.html - 글목록
                
                post_search.html - 글찾기
