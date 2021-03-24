# Google Scholar Azure

Project is Development

FPT University 


# Settings

```

#Setting Environment

1. Python (https://www.python.org/)

2.Anaconda (https://www.anaconda.com/)

3. Virtualenv (https://virtualenv.pypa.io/en/latest/)

> virtualenv env -> . env\Scripts\activate or (cd env\Scripts and input: activate)


## Settings

Delete Foder .azure (googleScholarAzure/)

git clone https://github.com/giakinh0823/googleScholarAzure.git

cd googleScholarAzure

pip install azure==4.0.0
pip install django-storages==1.11.1
pip install django-filter==2.4.0
pip install django-yearlessdate==1.3.1
pip install django-partial-date==1.3.1
pip install pandas==1.2.1
pip install selenium==3.141.0
pip install nltk
python -m pip install Pillow

> pip install -r requirements.txt


#Azure:

Signup in here: [Azure](https://azure.microsoft.com/en-us/)

1.Go to SQL Database

2.Create a Database

3.Go to Setting.py in project (googleScholarAzure/Scholar/setting.py)

4.Edit code Database:
 
[

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': '{name database}',
        'USER': 'Your User',
        'PASSWORD': 'Your password',
        'HOST': 'tcp:{Your SQL server}.database.windows.net',
        'PORT': '',
        'OPTIONS': {
            'unicode_results':True,
            'extra_params': 'ClientCharset=utf8',
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}


]


5.Go to Data Storages(Storage accounts)

6.Create a Data Storages

7.Edit code Data Storages:

[

AZURE_ACCOUNT_NAME = 'Your name data storages' #go to Access keys and show key
AZURE_ACCOUNT_KEY = 'Your key data storanges' #go to Access keys and show key

STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
DEFAULT_FILE_STORAGE = 'Scholar.custom_azure.AzureMediaStorage'

STATIC_LOCATION = "static"
MEDIA_LOCATION = "http://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/media"
MEDIA_ROOT='http://{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

AZURE_LOCATION = 'name Containers' # go to Containers to get the key
AZURE_CONTAINER = 'name Containers' # go to Containers to get the key

STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'

]


## Run code

# 1. localhost: 

> python manag.py runserver


# 2. Azure:

2. 

> python --version

example: Python 3.9.1

-> edit file runtime.txt in (googleScholarAzure/Scholar/runtime.txt)

-> Python-3.9.1

 
3.Go to Github (https://github.com/) create a new project 

4.Commit googleScholarAzure to your git

5. > az login (login)

6. > python manage.py runserver

7. > az webapp up --sku B1 --name <app-name>

8. > az webapp up

[Document](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python) 

```

## End
