# Disruptive News Detector

It is an attempt to build a tool that can take news inputs from various inputs like news websites, news feeds etc. It then further analyze the disruptive news to check its affect in market on the stock price of that company. It will present you 2 graphs - 1) Graph that shows severity of the disruptive news 2) Stock price of the company for that time period

It reads news to detect any disruptive news about a company.
There are 2 modes to run it (driven by settings)- 1) Batch Mode and 2) Continous Monitoring

1) Batch Mode - It reads already stored news from a folder and process them. It shows on graph the disruptive news
    severity. Along with it, it pulls the stock price for that company during that time period. Trying to depict
    the affect of disruptive news on its stock price.

2) Continous Monitoring - We can run the program to process live news feed. As soon as news is dropped in a folder,
    it will be processed, stock process are pulled to show the affect of news.

Before running this project, please make sure you have all the required python modules installed.
It has Python 3.x dependency defined. To install python libraries, run below command:
(make sure 'requirements.txt' file is available where you are running it )

pip3 install -r requirements.txt
