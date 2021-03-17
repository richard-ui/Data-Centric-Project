# Data Centric Project

## Rick's Restaurants

- Link to Project - [View](https://rickys-recipe-manager.herokuapp.com/)

![All_Devices](/static/img/big_chief.jpg)

# Brief Introduction to the Project

The purpose of this project is to create a virtual recipe website that uses a database of recipes which can be 
searched, viewed, added, deleted and updated.

# UX User Stories

### First Time User's:

- As a First Time user, I want to understand the main concept of the site and learn the intention of its relevance.

- As a First time user, I want to be able to navigate the site in an easy and efficient way without any complex design.

- As a First Time user, I want to be able to register

- As a First Time user, I want to be able to browse and search for recipes 

- As a First Time user, I want to get inspiration for a recipe to make myself.

### Returning User's:

- As a returning user, I want to be able to log in easily and efficiently. 

- As a returning user, I want to be able to view my recipes on my own profile page. 

- As a returning user, I want to be able to edit my existing recipes.

- As a returning user, I want to be able to delete existing recipes.

- As a returning user, I want to be able to add new recipes 

- As a returning user I want to be able to search a recipe from an input box and see suggestions depending on which letters I type. 

### Admin goals: 

- As an Admin, I want recipes added via the site to be stored in the correct format in the database 

- As an Admin, I want to be able to see who has added each recipe. 

# Design

1. Colour Scheme
- The two main colours on the site are bright, creating a vibrant feeling for the user throughout. Using dark font for headings/links contrasted nicely with the flow of the page.

2. Typography
- The 'Lucida Bright' font is the main font used throughout the website with Times and Serif as the fallback fonts in case for any reason the font is not supported by the browser.

# Wireframes

- Computer Wireframe - [View](https://github.com/richard-ui/interactive-milestone-project/tree/master/assets/wireframes/MapPage.pdf) 

- Mobile Wireframe - [View](https://github.com/richard-ui/interactive-milestone-project/tree/master/assets/wireframes/Mobile.pdf)

# Technologies Used

1. Bootstrap 4.5
2. Google Chrome
3. Materialize 
4. JavaScript 
5. Font Awesome
6. jQuery
7. Git
8. GitHub
9. Gitpod
10. Balsamiq
11. Python and Python3
12. Flask
13. MongoDB
14. Heroku
15. Jinja

# Features
| Feature  | Details |
| ------------- | ------------- |
| Register  | The User can create an account which will be saved to the database and used to login for future use.   |
| Login  | The user can log into their own account with personalised features.  |
| Log out  | There is a log out functionality on the page - this is especially important for users of a shared device.   |
| Add recipe   | Users can contribute to the site via the add recipe form.  |
| Edit recipe form | Users are able to edit their own recipes. An important note here is that users can only edit their own recipes.   |
| Delete recipe   | Users are able to delete their own recipes. As above, this can only be done with the user's own recipes.  |
| Search function   | The users are able to search the recipe database by ingredient and recipe name. This function is available whether a user is logged in/registered or not.  |

# Bugs
- There was an issue displaying the image for each recipe as it was not appearing as it should in the img tag. A solution to this, I did some research and figured that 
  When using Flask you cannot embed template tags inside other template tags as this causes an error. Therefore i replaced 

'<img id="imgdata" src="{{ url_for('static', filename='img/'{{ recipe.file }} }}">' with '<img id="imgdata" src="{{ url_for('static', filename='img/') }}{{ recipe.file }}">'


# Testing

### User Testing for User Stories
### First Time User's:

- As a First Time user, I want to understand the main concept of the site and learn the intention of its relevance.

  i. Upon entering the site, it is clear to the user that the website is about food, due to the sites vibrant colours and clear
  background image of food displayed on the body.
  
  ii. These links are also dynamic as specific links will be shown depending on whether the user is logged in or not.

- As a First time user, I want to be able to navigate the site in an easy and efficient way without any complex design.

  i. The navigation is clear and bright using bold text for the linksto identify each.
  
  ii. These links are also dynamic as specific links will be shown depending on whether the user is logged in or not.

- As a First Time user, I want to be able to register

  i. In the navbar a link named register that when clicked will take the user to the register page.

  ii. They will then create using a username and password

- As a First Time user, I want to be able to browse and search for recipes.

  i. A card is displayed on the homepage allowing me to type in a recipe and click the seasrch button beside it.
  Recipes will display below.
  
  ii. If no recipes are found a "No results found" message will warn the user immediately.

- As a First Time user, I want to get inspiration for a recipe to make myself.

  i. The images have an effect on what food the user may desire
  
  ii. The Cuisines list in the dropdown provide nationalities, as they view them, they can think of recipes from one of these Countrie's.

### Returning User's:

- As a returning user, I want to be able to log in easily and efficiently.
  
  i.  In the navbar a link named 'login' will take me to the login page.

  ii. If they are a registered user, typing in their username and password will log them in.

- As a returning user, I want to be able to view my recipes on my own profile page.

  i. Created recipes made by the user can be displayed on the recipes/home page or their profile page once logged in.

- As a returning user, I want to be able to edit my existing recipes.

  i. All my recipes on the recipes page provide edit buttons.

  ii. When the edit button is clicked, this will take me to the edit recipe page with existing data displayed in the input boxes.

  iii. This will allow me to update multiple values, after the edit button is clicked, all values for that recipe will be updated.

- As a returning user, I want to be able to delete existing recipes.

  i. For each recipe a red delete button will be displayed below it. When pressed, a modal will appear asking for confirmation of deletion.

- As a returning user, I want to be able to add new recipes.

  i. A form allows for user input with creating a new recipe, inlcluding name, image and cuisine.

- As a returning user I want to be able to search a recipe from an input box and see suggestions depending on which letters I type.


### Further Testing

- The W3C Markup Validator was a feature used to validate all html elements on each page.

- Whereas the W3C CSS Validator Services were used to validate every snippet of css in the style sheet.

- JSHint was used to validate all the JavaScript code within each file.

- The website was tested on multiple browsers such as Microsoft Edge, Opera and FireFox, but the main one that was used was Chrome. This was because I was using the chrome extension at the time for gitpod and I felt chrome was fast and reliable.

- The website was viewed on iPhone, Android, Laptop and Desktop Devices. There was also use of the developer tools as a faster way to look at the site becoming responsive such as using the example devices in the tools area. Friends and family members were asked to review the site and documentation to point out any bugs and/or user experience issues.

- The Responsinator tool was a feature used to view the deployed site and look to see how each device would display it. Device screens such as Android, iPhone and iPads were used to view on. In doing so they were viewed in a landscape and portrait perspective.


# Deployment

## Github Pages

1. Log in to GitHub
2. Locate the repositories and chose one that you want to Deploy
3. Press the "Settings"
4. Scroll down to the GitHub pages section
5. Under "Source" enter the drop down list with the first value of "None" and select "Master branch" instead
6. The page will refresh to be took to the top of the page
7. Scroll down until you get to the "Github pages" section to identify your now deployed link to your website

# Content
- The images of each recipes came from Google images, using the Advanced search setting.
- BBC good food website for recipe idea's and content.

# Credits
- Made use of code from websites such as stack overflow and geeksforgeeks.com

# Acknowledgements
- Holly-ford Github. It Provided me help to submit an array of ingredients/steps to the database using jQuery.
- My Mentor provided me with help and provided me access to Holly’s repository to view. This allowed me to locate the issues in my code and improve functionality that I may have been struggling with.

 My friends and family who helped to test the site and to add recipes 

- Girlfriend - Alexandra Connolly 

- Father – Gary Jones 

- Friend – Ashley Wilson 
