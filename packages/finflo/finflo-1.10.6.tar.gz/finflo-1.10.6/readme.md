# SCF_FSM_PACKAGE

A resuable python django package that can handle transition and workflow's in your django application .

## Description
- The finflo package is designed to take over all the complexity in FSM building for a workflow scenario
- Your transition's are made easy with finflo
- customizable Actions and states with on_flow interchangable

## Authors

- [@anandrajB](https://github.com/anandrajB)
- [@Mohamed-Sheik-Ali](https://github.com/Mohamed-Sheik-Ali)

## Prerequisite
- python
- Django
- Django-rest-framework

## 1. Installation 

### 1.1 Initial setup

- Install finflo using pip

```bash
pip install finflo
```

- In your django application , browse to installed_apps section in settings.py and add this ,

```bash
INSTALLED_APPS = [
    'finflo',
    'rest_framework'
]
```
- Add this in your settings.py 

```bash
FINFLO = {
    'WORK_MODEL' : ['MyApp.Model','MyApp2.Model2']
}
```

- Navigate to the middleware section in your settings.py and add the finflo middleware

```
MIDDLEWARE = [
    'finflo.middleware.TransitionUserMiddleware',
]
```

- Now add this peice of code in your urls.py

```
urlpatterns = [
    path('', include('finflo.urls'))
]
```
### 1.2 Migrations

- once all the steps done from the above section 1.1 .
- now we can apply the migrations for the database using ,
```
- python manage.py makemigrations
```
```
- python manage.py migrate 
```

### 1.3 Re-migrate
- ***scenario 1*** : if any new values is added to the **WORK_MODEL** 
- ***example for scenario 1 :***
```
# see 1.1 

FINFLO = {
    'WORK_MODEL' : ['MyApp.Model','MyApp2.Model2','MyApp3.Model3']
}

```
- you can remigrate the database without droping it using the below command .
```
- python manage.py migrate finflo 0002
```

## Usage


1. Once your setup is completed , whenever the objects in **WORK_MODEL** is created , the finflo automatically creates :
    
    - Transition manager
    - workflowitems 
    - workevents

2. The transition for each model can be carried out with :
    - t_id (transition_id)
    - type (model_type)
    - action 
    - example
    - ![Screenshot](finflo_postman.PNG)


3.  Some important information for transition are as follows :
    
    |  Arguments   | Data_Type  |
    | ------------- | ------------- |
    | type   | str  |
    | action  | str  |
    | t_id | int  | 
    | source (optional) | str  | 
    | interim (optional) | str  | 
    | target (optional) | str  | 
    | from_party (optional) | str  | 
    | to_party (optional) | str  | 




## Additional API's 

#### Api urls 


| Api URL's  | METHOD | QUERY_PARAMS |
| ------------- | ------------- | ------------- |
| *localhost/model/* | GET  | ?type=PROGRAM & t_id = 1|
| *localhost/*action*/* | GET | NONE |
| *localhost/*action*/* | POST | NONE |
| *localhost/*workflowitems*/* | GET | NONE |
| *localhost/workevents/* | GET | NONE |




## Support

For support, email support@venzo.com .


