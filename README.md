# Project 1

Web Programming with Python and JavaScript

/python_importer:
  This directory houses the books.csv file given and the program import.py that
    connects to the database, creates the tables if not present, and imports the
    books list.

/templates:
  /api.html:
    This page returns the JSON data required given an ISBN, throwing a 404 error
      if not found in the database
  /book.html:
    This page comes after a search query by the user, simply showing the results
      relevant from the database; also allows for logout
  /error.html:
    Used in various cases with different messages to let the user know what's
      gone wrong; typically best to simply back out of; otherwise, you can link
      back to the homepage
  /index.html:
    The homepage here accepts a login or a registration into the site via a Bootstrap
      card component; relevant errors are thrown if the user does or doesn't exist,
      accordingly, suggesting a remedy
  /reviews.html:
    This page comes after a successful login, also allowing for a logout; it houses
      the search bar where users can search the database
  /template.html:
    A simple frame for which the other pages inherit from
  /title.html:
    This page exists for each title in the database, generally accessed via the search
      bar on reviews.html; it gives the book's relevant information, local reviews
      to the site and ratings, an option to leave your own review and rating (given
      that you haven't already), and then lastly the Goodreads information; at time
      of writing, the widget loads onto the page, but does not display as it should

/application.py:
  This is all of the flask logic for each of the sites, making the connections to
    the database, holding sessions for each user, and directing the routes for the site

/commands.txt:
  These are the relevant commands to get the app up and running locally; can be copied
    and pasted into the terminal

/k.txt:
  An encrypted file for the Goodreads key credentials; key ultimately hard-coded into
    the app, but could be used for central access and rolling new keys

/README.md:
  By now, you've seen what this one's got!

/requirements.txt:
  The required installs for the application; only one added was "Requests"



General Notes:
  Obviously the biggest improvements would be in UX/UI. Added navigation throughout
    the site would make navigation in actual use-cases much better. Also, styling is
    minimal to none for the most part. My wife and I left on Feb. 22nd to move to
    New Zealand from Texas, so I've had a little less time to flesh this project out
    compared to what the rest of them will get!

  Thanks so much,
  Matthew Smith
