# Final project: Find your next favorite movie!

## Quick Summary

This application allows users to register and sign in to their own personal movies collection. They'll be able to search for any movie on TMDb and see the ratings and movie info that they search for. They can also look for any actor for their filmography and add it to a personal collection. They'll be able to personally rate the movies that they watch, and will have 3 sections: saved directors, saved actors, and saved movies. 

## How to use the program

The user will need to first log into their google account for the program to work. They will follow the log in link to do so. After that, they can either choose to look up a movie or look up an actor. For example, they can type in "Baby Driver" in the first stringfield. This will bring them to a page with a potential list of movies and their description. The user saves the movie they want to save, which will bring them to their list of movies. From here, they can personally rate the movie once they've seen it by typing their rating into the stringfield provided for each movie. The same occurs for the actor searchbar, minus the rating part.

## Modules

No additional modules are used

## Routes:

* / --> index.html
* /all_actors --> all_actors.html
* /all_directors --> all_directors.html
* /all_movies --> all_movies.html
* /movie_results --> loads the search data from movies form
* /movie/<id> --> processes the data and redirects to /all_movies
* /actor_results --> loads the search data from actors form
* /actor/<id> --> process the data and redirects to /all_actors
* /update/<movie> --> updates movie rating, redirects to /all_movies
* /delete/<movie> --> deletes movie object from db


## Checklist:

 **user should be able to load http://localhost:5000 and see the first page they ought to see on the application.**

 **Include navigation in base.html with links (using a href tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, like this )**

 **Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.**

 **Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).**

 **Must have data associated with a user and at least 2 routes besides logout that can only be seen by logged-in users.**

 **At least 3 model classes besides the User class.**

 **At least one one:many relationship that works properly built between 2 models.**

 **At least one many:many relationship that works properly built between 2 models.**

 **Successfully save data to each table.**

 **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).**

 **At least one query of data using an .all() method and send the results of that query to a template.**

 **At least one query of data using a .filter_by(... and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).**

 **At least one helper function that is not a get_or_create function should be defined and invoked in the application.**

 **At least two get_or_create functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).**

 **At least one error handler for a 404 error and a corresponding template.**

 **At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.**

 **Include at least 4 template .html files in addition to the error handling template files.**

 **At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.**

 **At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that does accord with other involved sites' Terms of Service, etc).**

 **Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source to the database (in some way).**

 **At least one WTForm that sends data with a GET request to a new page.**

 **At least one WTForm that sends data with a POST request to the same page. (NOT counting the login or registration forms provided for you in class.)**

 **At least one WTForm that sends data with a POST request to a new page. (NOT counting the login or registration forms provided for you in class.)**

 **At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.**

 **Include at least one way to update items saved in the database in the application (like in HW5).**

 **Include at least one way to delete items saved in the database in the application (also like in HW5).**

 **Include at least one use of redirect.**

 **Include at least two uses of url_for. (HINT: Likely you'll need to use this several times, really.)**

 **Have at least 5 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.)**

Additional Requirements for additional points -- an app with extra functionality!
Note: Maximum possible % is 102%.

 (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.

 **(100 points) Create, run, and commit at least one migration.**

 (100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)

 (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)

 **(100 points) Implement user sign-in with OAuth (from any other service), and include that you need a specific-service account in the README, in the same section as the list of modules that must be installed.**
