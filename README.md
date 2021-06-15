 3D Printing Management Web App 

 Note: This was setup in Windows so steps for Linux or Mac might differ 
 and will need to be researched (Sorry) 

 Prerequisites 
  - Need to have python installed (preferrabley version 3.8 or greater) 
  - You can install Django with pip: run the command -> pip install Django 
  - pip install python-dotenv
  - pip install django-bootstrap4
  - add a .env file at the root directory and paste secret key in variable 
   SECRET_KEY=


 Useful Django commands 
  - to run the local server with the app (be in root directory) -
                     -> python manage.py runserver 
  - to start a new app in the project -> python manage.py startapp appName 
  - 

 Way of Working
 It is recommended to create your branch for working on the project. 
 When there is something we want to merge into main branch create a pull request 
 and all the members will review the changes 

 Coding Standard 
 I like to lightly follow pep8 python standard of coding for consistency. 
 For now, the main things I started is using mixedCase for variable names and 
 documenting your functions 
 We can always discuss if anything in particular needs to change or be added 

 Django Framework 
 The way Django frames a web app is one folder/app (PrintSystem) forms the core of the
 settings for the webapp. Here you can find the html returned by the apis(views) 
 and the the settings of the project and the urls that users will be able to access 
 These two files are the ones we will mostly modify


 The folder JobTracker were created with python manage.py startapp appName
 They represent different functionalities of the web app with their associated models(database data) and
 views(apis) and templates(html) 

 Each app also has a model file which contains the database classes (these classes are mapped to a 
 sql database in sqlite3) Then these models are captured by the views.py (apis) to return the 
 required html in the templates folder to the front end 

 you can also run -> python manage.py migrate    --> to update the schemas for the databases after 
 you update the models

 I also installed bootstrap 4 which has to be loaded to each new html (see base.html for e.g) 
 which can be used to format the html 
 You can also include css, imgs and javascript by including it in the folder static inside each app

 Feel free to get comfortable and play around with the code 
 

