# DJANGO OUTBOX ENCRYPTION

Sometimes, when you ready to publish your project to server. 

There is a slight change between the application settings on the local and the server.
Such as database name, password, etc.
The second thing, is you need to encrypt information like password or other.
The last one, you need to automatically select setting local when you work on local computer, and auto select server when application running on server.

You are on the right path...


## Install package to your environment
    > pip install outbox-encryption

## How to use 

### Encrypt to environment
    This code for create ".env.client" or ".env.server" file    
    > python manage.py shell

    > from encryption import OutboxEncryption
    > lib = OutboxEncryption()
    > mplaint_text = {
            'DB_PASSWORD': '',
            'SECRET_KEY': 'xxg_7me8rl2m#a_h2oresgt2#ni=3_4*!ai*=rtsq)yi!g7_5-51xx'
        }
    > lib.encrypt_environ('.env.local', mplaint_text)
    # file .env.local is created (maybe file is hidden, CTRL+H to show it)

    # Open file .env.local
        You have to write other setting that no encrypt apply, such as:
        DEBUG=True
        UNDER_CONSTRUCTION=False
        DB_ENGINE=django.db.backends.mysql
        DB_NAME=db_name
        DB_USER=root
        DB_HOST=127.0.0.1
        DB_PORT=3306

#### Note:
    File .env.local must be :
        .env.local or
        .env.server (nothing else)

### Decrypt from environment 
    Run inside settings.py (django project settings)            
    > from encryption import OutboxEncryption
    > lib = OutboxEncryption()

    Setting unique variable that only exists in local environment, and not exist in server 
    We choose env_outbox_encrypt
    > lib.set_keyword_local('env_outbox_encrypt')

    List of key variable that must be encrypt or decrypt before set or get data
    > mplaint_key = ['DB_PASSWORD', 'SECRET_KEY']

    Variable that must be cast as list from environmnet to settings.py
    > mplaint_list = ['ALLOWED_HOSTS']

    Variable that must be cast as tuple from environment to settings.py
    > mplaint_tuple = ['SECURE_PROXY_SSL_HEADER']

    Get encryption data
    > dict1 = lib.decrypt_environ(mplaint_key, mplaint_list, mplaint_tuple)

    Setting variable :
    > DEBUG = dict1['DEBUG']
    > UNDER_CONSTRUCTION = dict1['UNDER_CONSTRUCTION']
    > DEBUG = dict1['DEBUG']
    > SECRET_KEY = dict1['SECRET_KEY']
    > ALLOWED_HOSTS = dict1['ALLOWED_HOSTS']
    > DATABASES = {
        'default': {
            'ENGINE'    : dict1['DB_ENGINE'],
            'NAME'      : dict1['DB_NAME'],
            'USER'      : dict1['DB_USER'],
            'PASSWORD'  : dict1['DB_PASSWORD'],
            'HOST'      : dict1['DB_HOST'],
            'PORT'      : dict1['DB_PORT'],
        }
    > SECURE_PROXY_SSL_HEADER = dict1['SECURE_PROXY_SSL_HEADER']



    
    
