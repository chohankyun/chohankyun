# [chohankyun.com](http://chohankyun.com)
python, django, djangorestframework, allauth, rest-auth, html, angularjs, bootstrap  


## devlopment    
--OS--   
windows  

--web server--  
builtin Django webserver  

--interpreter--  
python 3.6 later

--DB--  
mariadb  

--IDE--  
pycharm professional   

## operation  
--OS--   
ubuntu    

--web server--  
apache  

--interpreter--  
python 3.6 later

--db--  
mariadb  
 
## software  
--server--  
* python
* django
* djangorestframework

--server libs--  
* referenced by requirements.txt

--client--  
* angularjs
* jquery
* bootstrap
* html

--client libs--  
* referenced by index.html

--reference client--
* Tivix/angular-django-registration-auth (github.com)

--email smtp--  
* gmail  

****

### 설명  
chohankyun.com 사이트를 만들기 위한 소스입니다.  
기본적으로 python, django, djangorestframework, angularjs, bootstrap 를 사용해서 작성되었습니다.   
또한 여러가지 오픈 소스를 기반으로 작성 되었으며, 몇가지 오픈소스는 사이트에 맞게 수정했습니다.   
라이센스는 MIT 라이센스를 적용했습니다.   

### 기능  
* 로그인 관리   
* 회원 관리   
* 홈 화면  
* 게시물 리스트    
* 게시물 관리    
* 댓글 관리  
* 추천 관리    
* 검색  
* 다국어 처리(영어, 한국어)  

### 참고   
* 여러가지 오픈소스를 기반으로 만들다 보니 오픈소스가 대부분은 MIT 라이센스 인데 일부 오픈소스는 라이센스 관련 내용이 없는것도 있었습니다.  
* 이미지 및 동영상은 url 입력으로만 가능 합니다.

### 문제
사용된 프레임워크와 오픈소스를 완벽하게 이해하고 만든것이 아니라 약간의 문제가 있을 수 있습니다.      
만약 문제 되는 부분이 있거나 혹은 문의 사항이 있으면 연락주세요.  

### 연락처  
<chohankyun@gmail.com>  


****
## 개발환경
### windows
* python 3.6 later 설치  
* pycharm professional   
* mariadb 설치 (utf-8 설정)  
* git 설치 (utf-8 및 unix 설정)  

### pycharm 설정
* 초기화면 > configure > settings > appearance & behavior > appearance 의 theme 를 darcula 설정  
* 초기화면 > configure > settings > keymap 은 Eclipse 설정   
   
      Run manage.py Task 를 ctl + alt + r 로 설정  

* 초기화면 > configure > settings > editor > code style 의 line separator를 unix and os x(\n) 설정    
* 초기화면 > configure > settings > editor > code style 의 right margin (columns) 를 300 설정 (저의 화면은 4k)  
* 초기화면 > configure > settings > editor > code style 의 file encoding 은 모두 utf-8 설정   
* 초기화면 > configure > settings > plugins 에서 .ignore 설치
* 초기화면 > configure > settings > version control > git 설정
* 초기화면 > configure > settings > version control > github 설정
* 초기화면 > configure > settings > project > project interpreter 에서 virtualenv 추가
* 초기화면 > ckeck out from version control > git or github 선택 (git clone)   

      git repository url : https://github.com/chohankyun/chohankyun.git 
      parent directory : c:\work\projects
      directory name : chohankyun  
      
* 프로젝트 > chohankyun > requirements.txt 파일 클릭
    
      requirements.txt 의 모듈 설치
    
 ### mariadb 설정  
 * root 로그인
 * data_db (utf-8) 데이터베이스 생성
 * data_user 사용자 생성 
 
       data_user 생성 시 data_db 만 참조 및 전체권한 부여
   
### windows 환경변수 설정  
* 프로젝트 > chohankyun > chohankyun > settings.py 파일의 환경 변수 확인
* os.environ['DB_HOST'] 을 위한 windows 환경변수 DB_HOST=127.0.0.1
* os.environ['DB_PASSWORD'] 을 위한 windows 환경변수 DB_PASSWORD=*********
* os.environ['EMAIL_HOST_PASSWORD'] 을 위한 windows 환경변수 EMAIL_HOST_PASSWORD=********

### log 폴더 생성  
* window 탐색기 상에서 chohankyun 같은 레벨에 log 폴더 생성
  
      상위폴더/chohankyun
      상위폴더/log
  
### django 초기화  
* run manage.py task 실행 (ctl + alt + r)  
* db table 생성
  
      makemigrations : 테이블 스키마 생성
      migrate : 테이블 생성
      
 * admin 사용자 생성
    
       createsuperuser : 슈퍼유저 생성
       
 * 다국어 처리 파일 생성
   
       compilemessages : 다국어 파일 컴파일
    
### 사이트 초기화
* 프로젝트 > chohankyun > static > favicon.ico 수정
* 프로젝트 > chohankyun > static > logo.png 수정
* builtin Django webserver 실행
* http://127.0.0.1:8000/admin
* admin 로그인
    
      board > catagorys 추가
      home > carousels 이미지 경로 추가 
      index > footer 추가
      index > header 추가

****
## 운영환경  
### cloud (aws - amazon web service)
* route53
* ELB (Elastic Load Balancing)  
* EC2 (Elastic Compute Cloud) 

### EC2
* Elastic IP 할당
* security group  
      
      http 추가
      mysql 추가

### ubuntu 언어 설정 
* sudo apt-get update
* sudo apt-get install language-pack-ko
* sudo locale-gen ko_KR.UTF-8
* sudo dpkg-reconfigure locales
* sudo update-locale LANG=ko_KR.UTF-8 LANGUAGE=ko_KR:ko
* sudo dpkg-reconfigure tzdata

### python3.6 설치 / 설정 
* sudo add-apt-repository ppa:jonathonf/python-3.6
* sudo apt-get update
* sudo apt-get install python3.6
* sudo apt-get install python3-pip
* sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
* sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
* sudo update-alternatives --config python3

      python3.6 선택
   
* pip3 -V
* sudo ln -f -s /usr/bin/python3 /usr/bin/python
* sudo ln -s /usr/bin/pip3 /usr/bin/pip

### apache2 와 mod_wsgi for python3.6 설치
* sudo apt-get install apache2
* sudo apachectl stop
* sudo apt-get install apache2-dev
* sudo apt-get install python3.6-dev
* sudo pip install mod_wsgi
* cd /etc/apache2/mods-available
* sudo vi wsgi_express.load

      LoadModule wsgi_module /usr/local/lib/python3.6/dist-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so

* cd /etc/apache2/mods-enabled
* sudo ln -f -s ../mods-available/wsgi_express.load wsgi_express.load

### github 연동
* cd
* cd .ssh
* ssh-keygen -t rsa -C “email 주소”
* github > chohankyun / chohankyun > Deploy keys 에 public key 등록
* cd
* mkdir app
* git clone git@github.com:chohankyun/chohankyun.git web
* cd web
* sudo pip install -r requirements.txt

### log 폴더 생성
* app 폴더 아래에 log  폴더 생성
* /home/ubuntu/app
* mkdir log
     
      app/web
      app/log

### apache2 와 django 연동 (deamon mode)  
* cd /etc/apache2/sites-available
* sudo vi chohankyun.conf

      <VirtualHost *:80>
              ServerName www.chohankyun.com
              ServerAlias chohankyun.com
              ServerAdmin webmaster@localhost
              DocumentRoot /home/ubuntu/app/web/

              ErrorLog ${APACHE_LOG_DIR}/error.log
              CustomLog ${APACHE_LOG_DIR}/access.log combined

              <Directory /home/ubuntu/app/web/>
                     Order allow,deny
                     Allow from all
              </Directory>

              WSGIDaemonProcess chohankyun.com user=ubuntu group=ubuntu python-path=/home/ubuntu/app/web
              WSGIProcessGroup chohankyun.com

              WSGIScriptAlias / /home/ubuntu/app/web/chohankyun/wsgi.py

              <Directory /home/ubuntu/app/web/chohankyun/>
                      <Files wsgi.py>
                             Allow from all
                             Require all granted
                      </Files>
              </Directory>

              Alias /static/admin/ /usr/local/lib/python3.6/dist-packages/django/contrib/admin/static/admin/

              <Directory /usr/local/lib/python3.6/dist-packages/django/contrib/admin/static/admin/>
                     Allow from all
                     Require all granted
              </Directory>

              Alias /static/ /home/ubuntu/app/web/static/

              <Directory /home/ubuntu/app/web/static/>
                     Allow from all
                     Require all granted
              </Directory>

              Alias /media/ /home/ubuntu/app/web/media/

              <Directory /home/ubuntu/app/web/media/>
                     Allow from all
                     Require all granted
              </Directory>
      </VirtualHost>
          
               WSGISocketPrefix /var/run/wsgi
        
* cd /etc/apache2/sites-enabeled
* sudo ln -f -s ../sites-available/chohankyun.conf chohankyun.conf
* sudo rm 000-default.conf

### mariadb 설치
* sudo apt-get install mariadb-server
* cd /etc/mysql
* sudo vi mariadb.cnf
* 아래 내용 추가
     
      [mysqld]
      collation-server = utf8_unicode_ci
      init-connect='SET NAMES utf8'
      character-set-server = utf8
      bind-address = 0.0.0.0

      [client]
      default-character-set=utf8
      
* sudo service mysql restart
* sudo mysql -u root
        
      create database data_db;
      create user 'data_user'@'%' identified by '비밀번호';
      grant all privileges on data_db.* to data_user@'%';
      flush privileges;
      
### ubuntu 와 apache 환경변수 설정  
* 프로젝트 > chohankyun > chohankyun > settings.py 파일의 환경 변수 확인
* os.environ['DB_HOST'] 
* os.environ['DB_PASSWORD'] 
* os.environ['EMAIL_HOST_PASSWORD']
* cd
* vi .profile
* 아래 내용 추가

      export DB_HOST='127.0.0.1'
      export DB_PASSWORD='*********'
      export EMAIL_HOST_PASSWORD='**********'
      
 * . .profile
 * cd /etc/apache2
 * sudo vi envvars
 * 아래 내용 수정 및 추가
 
       #export LANG=C
       export LANG=ko_KR.UTF-8
       export LC_ALL=ko_KR.UTF-8
       export LANGUAGE=ko_KR:ko
       
       export DB_HOST='127.0.0.1'
       export DB_PASSWORD='********'
       export EMAIL_HOST_PASSWORD='*********'
       
 * sudo apachectl stop
 * sudo apachectl start
 
 
 ### django 초기화  
* cd /app/web
* db table 생성
  
      python manage.py makemigrations : 테이블 스키마 생성
      python manage.py migrate : 테이블 생성
      
 * admin 사용자 생성
    
       python manage.py createsuperuser : 슈퍼유저 생성
       
 * 다국어 처리 파일 생성
   
       python manage.py compilemessages : 다국어 파일 컴파일
       
### 사이트 초기화
* 프로젝트 > chohankyun > static > favicon.ico 수정
* 프로젝트 > chohankyun > static > logo.png 수정
* http://사이트주소/admin
* admin 로그인

      board > catagorys 추가
      home > carousels 이미지 경로 추가 
      index > footer / header 추가
 


 
      





