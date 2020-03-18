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
* 현재 여러가지 이유로 "DEBUG = True" 로 동작 하고 있습니다.

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
* gettext 설치 (다국어 처리)

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
      사이트 > 사이트들 수정 (default:example.com )

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

### ntp 동기화 설정 
* sudo apt-get ntp  
* sudo vi /etc/ntp.conf
* 기존내용 주석처리 
* 아래 내용 추가

    pool 1.kr.pool.ntp.org iburst  
    pool 1.asia.pool.ntp.org iburst  
    pool 2.asia.pool.ntp.org iburst  

* sudo service ntp restart  

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
* cd app
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
              
              # for search
              AllowEncodedSlashes On
              
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
       
 * sudo apachectl start
 
### django 초기화  
* cd /home/ubuntu/app/web
* db table 생성
  
      python manage.py makemigrations : 테이블 스키마 생성
      python manage.py migrate : 테이블 생성
      
 * admin 사용자 생성
    
       python manage.py createsuperuser : 슈퍼유저 생성
       
 * 다국어 처리 파일 생성
   
       python manage.py compilemessages : 다국어 파일 컴파일
       
### EC2 만 사용
* 브라우저에서 elastic ip 로 접근 

### 도메인을 EC2 에 직접 연결 후 사용
* 도메인 구입 사이트의 관리 페이지에서 DNS 에 A(address) record 추가 (가비아)

      타입: A , 호스트 : @  ,  값 : elastic ip
      타임: A , 호스트 : *  ,  값 : elastic ip
      
* 브라우저에서 도메인으로 접근   
   
      http://chohankyun.com
      http://www.chohankyun.com

### elb (ssl 인증서), ec2 구성
* aws 에서 발행하는 인증서 생성

      chohankyun.com
      *.chohankyun.com (추가 도메인)
      
* e-mail 인증을 사용하고, 위의 두개의 도메인을 포함 하는 인증서 생성    
* elb 생성 시 https 리스너 추가하고, 생성 된 ssl 를 추가
* elb 생성 후 elb dns 주소로 접속 테스트
  
      http://elb dns 주소 
       
* 도메인 발급 회사의 dns 설정 화면에서 cname 레코드 등록
* cname 으로 elb 등록 (가비아)

      타입: cname , 호스트 : @  ,  값 : elb dns 주소 (끝에 "."  추가)
      타임: cname , 호스트 : *  ,  값 : elb dns 주소 (끝에 "."  추가)
      
* http 테스트 
      
      http://chohankyun.com
      http://www.chohankyun.com
      
* https 테스트

      https://chohankyun.com
      https://www.chohankyun.com
      
* http 요청 시 https 로 redirect 변경을 위한 rewite 모듈 로드
     
      ec2 ssh 접속
      cd /etc/apache2
      cd mods-enabled
      sudo ln -f -s ../mods-available/rewrite.load rewrite.load
      
 
* http 요청 시 https 로 redirect 변경을 위한 apache2 설정 변경
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
              
              # for search
              AllowEncodedSlashes On 
              
              # for aws elb ssl
              RewriteEngine On
              RewriteCond %{HTTP:X-Forwarded-Proto} =http
              RewriteRule .* https://%{HTTP:Host}%{REQUEST_URI} [L,R=permanent]
            
      </VirtualHost>
              WSGISocketPrefix /var/run/wsgi
       
* sudo apachectl restart
  
### aws route53, elb (ssl 인증서), ec2 구성
* aws 에서 발행하는 인증서 생성

      chohankyun.com
      *.chohankyun.com (추가 도메인)
      
* e-mail 인증을 사용하고, 위의 두개의 도메인을 포함 하는 인증서 생성    
* elb 생성 시 https 리스너 추가하고, 생성 된 ssl 를 추가
* route53 에 도메인 등록
* route53 A record 로 elb 등록

      chohankyun.com     elb
      *.chohankyun.com   elb
      
* http 테스트 
      
      http://chohankyun.com
      http://www.chohankyun.com
      
* https 테스트

      https://chohankyun.com
      https://www.chohankyun.com
      
* http 요청 시 https 로 redirect 변경을 위한 rewite 모듈 로드
     
      ec2 ssh 접속
      cd /etc/apache2
      cd mods-enabled
      sudo ln -f -s ../mods-available/rewrite.load rewrite.load
      
 
* http 요청 시 https 로 redirect 변경을 위한 apache2 설정 변경
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
              
              # for search
              AllowEncodedSlashes On
              
              # for aws elb ssl
              RewriteEngine On
              RewriteCond %{HTTP:X-Forwarded-Proto} =http
              RewriteRule .* https://%{HTTP:Host}%{REQUEST_URI} [L,R=permanent]
            
      </VirtualHost>
              WSGISocketPrefix /var/run/wsgi
       
* sudo apachectl restart

### 사이트 초기화
* 프로젝트 > chohankyun > static > favicon.ico 수정
* 프로젝트 > chohankyun > static > logo.png 수정
* http://사이트주소/admin
* admin 로그인

      board > catagorys 추가
      home > carousels 이미지 경로 추가 
      index > footer / header 추가
      사이트 > 사이트들 수정 (default:example.com )
      

 


 
      





