# lis161project

For this project, we decided to create a website for the online applications of a college (in this case UP).

The functionalities of the website are as follows:
1. Allows users to create an account
2. Allows users to login
3. Allows users to fill out the college application form
4. Allows users to review their previously filled out application form
5. Allows users to edit and delete their application
6. Allows admins to view all applications
7. Alows admins to review, edit, and delete user applications
8. Allows admins to conduct searches of parameters of the application form

About:

  **Homepage**
  Contains basic information about the university and application process. The text was taken from the official UP online admissions website and formatted similarly. This page was made using basic html functionality and bootstrap.
  
  **Privacy Notice**
  Similar to the previous page, the text was taken from the official UP site and recreated using html and bootstrap
  
  **Navbar**
  The Navbar that is present on every page, was made using bootstrap. In contain 3 buttons and a dropdown menu. The 'University of the Philippines' takes the user back to the homepage. The 'Privacy Notice' button takes the user to the privacy notice page. The Online Application form has multiple functions based on the type of user. If not logged it, it prompts the user to login. If logged in, it takes the user to an unfilled application form. If the user has already filled out the form, then it takes them straight to the review of their form. Finally, this button takes admin users to the master list of all applications. The dropdown menu gives the users access to the register, login, and logout functionalities.
  
  **Registration System**
  In order to register, the user must provide an email and password. These get stored in the database as part of the 'accounts' table. When submitting credentials, a query is sent to the database to verify that the email is not already present in the database. If the email has already been used, the user will be redirected back to the registration page with an added message stating that the email has already been used. (email and password are not case sensitive)
  
  **Login System**
  The user is asked to submit an email and password. These are passed on as a database query. If the email-password pair are not present in the database, then the user will be redirected to the login page with a message stating their credentials are incorrect. If the email-password pair is present in the databse, 4 session variables (loggedin=True, account id, email, and type) are inititated. Logging out removes this session data.
  
  **Application Form**
  The application form is only available to logged in users. If not logged in, then the application form button redirects to the login page. The application form receives input from the user in the form of selection boxes and input fields. This data is then stored into the database under the 'applications' table. When accessing the application form, the website checks if the current user email (from the session data) is already present in the applications database. If it is not, then it redirects to a blank application form. If the email is present, the user is taken to a page to review the data of their application form. On this review page, they can choose to either edit or delete the application. Choosing edit takes them to the edit page. Here they can change any data of the form then update the data in the database. Deleting removes the application data from the database completely.
  
  **Admin Privileges**
  Admin users login by using the admin account (username: admin@up.edu.ph | pw: admin). When selecting the application form, admin users are instead taken to a master list containing all applications currently in the database. Admins can click on the name of the applicant to view their application form. Similarly, they can edit and delete users' application form. The masterlist also has a searchbar. The user selects a parameter (one of the preset fields present in the application form) and inputs a search query. This search query and parameter are taken by the database which returns all matches (note: this is case sensitive). If there are no matches, a message is displayed stating that there are no mathces. 
  
