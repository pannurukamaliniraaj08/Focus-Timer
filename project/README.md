# Focus Now
#### Video Demo:  https://youtu.be/oVjqYh0rTBo?si=gZwz8hHI5wWDCt5U
#### Description:

# Project Overview:
## Why I came across this idea:
    As someone who has wasted a lot of opportunities due to lack of time managment, distractions and doom-scrolling, it is realy important to keep track of what we are actually doing throughout the day or else we might end up thinking that we spent a lot of time on something, though we didn't. Hence, I created this web-application to give a reality-check to myself and people like me..
## About my project:
    This is a website where you get to keep track of your focused hours. If you are on a digital detox, you do not want cheap dopamine. Instead, we need real dopamine for real work. In this project, I have created different themes for different moods of the user with a timer that has pause & play feature with a dynamic background corresponding to the theme.
# File Breakdown:
## templates:
    Templates contains the html folders of the web-application.
* `apology.html`: For showing the apology messages in cases like, the username is entered incorrectly.
* `cyberpunk.html`: For the Cyberpunk theme along with stats.
* `dark.html`: For the Dark theme along with stats.
* `expresso.html`: For the Expresso theme along with stats.
* `forest.html`: For the Forest theme along with stats.
* `light.html`: For the Light theme along with stats.
* `pastel.html`: For the pastel theme along with stats.
* `index.html`: For showcasing all these themes.
* `layout.html`: Contains the basic layout of these themes.
* `login.html`: As the name suggests, it is for login page.
* `register.html`: As the name suggests, it is for register page.
## static:
    It contains all the pictures for the cards and video for making the timer dynamic along with **style.css** for other designs of the web-application.
### main.js:
    main.js is where the logic for timer i.e. start function, quit function and pause & play functions are written.
## helpers.py:
    The function of helper.py is similar to the helper.py of finance problem-set that includes login required and apology function.
## schema.sql & study.db:
     schema.sql contains the schema of study.db
* `users`: users TABLE for username, id, hash of the password and coins.
* `study_sessions`: study_sessions TABLE is essential for the bar graph of the focus time because this where the hours are taken from (duration_minutes is divided by 60).
* `purchases`: purchases TABLE to keep track of your purchases of themes made.
## app.py:
    This folder is similar to that of the function of app.py in finance.
* `imports`: Many third party libraries are imported in this this file to help me assist with many of my tasks.
* `register()`: This is the part the renders apology in case username is already used or if re-entered password doesn't match with the entered one and if everything goes well, it takes the password, hashes it, and inserts it into study.db along with username and gives you default value of coins to be "$0".
* `login()`: This is the part the checks if your entered username and password exist in the dataase, if not, it renders an apology(defined in helpers.py). If everything goes well, it takes you to index.html (the homepage).
* `light`: Since this is a default function, you would directly go the light mode timer and stats.
* `dark`: As the name suggests, this is a default function, you would directly go the dark-themed timer and stats.
* `other themes`: It contains **Cyberpunk**, **Forest**, **Pastel Sunset** and **Expresso Grind** themes. They do the same work but they would redirect you to **buy(theme)**, to check if you bought them.
* `buy(theme)`: As mentioned earlier, it checks if you have already bought it, if not, it would check, if you have enough money. If you have the capacity to buy it, then it would do that for you, deduce the money from your coins and store it in study.db. If you do not posses that ability to buy, then it would show you an error message from index.html using **showCoinToast(message)**.
* `get_seconds`: This where the information for your graphs come from.
* `get_daily_stats`: The data for the stats across the past 21 days, come from here. 21 days because, that's how long it takes to change a habit.

# MAJOR CHALLENGES:
## Timer Implementation:
### Design Choice:
    I decided to build a dynamic timer using JavaScript instead of constantly asking the server, so the page won't reload everysecond.
### Challenge:
    Syncing the timer with the video playing in the background, making it pause and play along with pause & play button and ensure the time was erased whenever the quit button pressed.
### Solution:
    Stored the data in a local storage before clearing the entire time data.
## Data Visualization (Graph):
### Design Choice:
    I wanted to show the user the progress, they have made in the past 21 days to keep them motivated.
### Challenge :
    Figuring out the design and code for the code.
### Solution:
    I used **Charts.js** where they had step-by-step guide for implementing the graphs and pie.
## UI Layout & Responsiveness:
### Design Choice:
    To implement a dashboard with timer and the graphs.
### Challenge:
    The graph stats started to act as child block of the timer
### Solution:
    Used CSS Flexbox/Grid containers with relative sizing so the graph scales dynamically based on screen width.

# Acknowledgements & Credits
* **Chart.js:** Used for rendering interactive data visualization graphs ([Chart.js Documentation](https://www.chartjs.org/)).
* **Bootstrap:** Used for UI components and responsive layout styling.
* **CS50x Staff:** For providing the course material, problem sets, and foundation for this project.
* **Pinterest:** For the images and video for cards and video of the timer.
