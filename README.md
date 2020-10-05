## Nasa Space Apps Challenge 2020 - Better Together

*You can find more details about the problem statement [here](https://2020.spaceappschallenge.org/challenges/confront/better-together/details).

# Please install the dependencies using pip in order to run the project:
1. geopy
2. nltk
3. tweet-preprocessor
4. pip install tweepy
5. htmldate

# Steps to run the project:
1. Open your terminal and navigate to the /webapp folder of the project.
2. Run command python manage.py makemigrations firstPage
3. Run command python manage.py migrate
4. To run the server: python manage.py runserver. Server runs on port 8000

-------------------------------------------------------------------------------------
# Description of our solution Ummeed

* [Demo Video](https://youtu.be/772L6VQiCBQ)  
* [Slides](https://docs.google.com/presentation/d/1rTvKWK-jaWbaJFMqfxpmxVO-QOqjVv74Wanipy7Ag6Y/edit?usp=sharing)

We developed a web application which acts a portal for communication and education and connects people all over the world to address various humanitarian issues occurring everyday. This is important because there is Inequality experienced by people all over the world and a general lack of awareness regarding urgent humanitarian issues. There is also an inability of socially aware people to contribute effectively. 

This was our motivation to approach this problem statement. Our solution helps bridge the gap that causes people to experience inequality and help address these issues. It will also help educate the users and get issues more outreach.

--------------------------------------------------------------------------------------
# Data and Resources:

NASA WorldWind SDK: Dependent on NASA and USGS satellite imagery, aerial photography, topographic maps, Keyhole Markup Language (KML) and Collada files.

Data Sources used to authenticate users claims:
- RSS Feeds
- News Organizations(Web Scraping)
- Twitter API

News Sources/RSS Feeds:
- Amnesty International
- UN Human Rights Feed
- NYU Human Rights Blog
- Chinese human Rights Defenders
- Google News

Technology:
- Html, CSS, JavaScript
- Django
- SQLite
- Python (Keyword Extraction, Document Similarity, Web Scraping and Twitter Analysis)
