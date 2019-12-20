## Team Details

Team members:
1)	Amit Agrawal (amita3@illinois.edu)
2)	Noushad Kunju-Muhammed (noushad2@illinois.edu)
3)	Mani Bayani(mbayani2@illinois.edu) - Group Leader

# Disruptive News Detector

Disruptive/Negative news coverage, such as poor earnings reports or stories of bad corporate governance, normally decreases demand, meaning more people want to sell the stock, thereby lowering the market price. Demand can also be negatively affected by news stories covering economic and political uncertainty, or unexpected, negative events.

In this project, we built a software to detect company-specific disruptive news and continuity of news from news articles in real-time and present the right discontinuity and severity information to the user. The software processes the news articles and predicts whether it is disruptive for the company, which is mentioned in the news article or not. It then further fetches the stock price of the company in real-time and try to show the coorelation between the negative news and stock price fluctuations. 

There are 2 modes to run it (driven by settings)- 1) Batch Mode and 2) Continous Monitoring

1) **Batch Mode** - In this mode, some news are already copied in the input folder. Program process each news one-by-one and determines if news is negative for a company or not and what is the severity level. It shows the news severity on graph. Along with it, it pulls the stock price of that company during that time period. Trying to show the coorelation between news and its stock price.

2) **Continuous Monitoring** - We can run the program to process live news feed. Program will monito for any new news dropped in an input folder. As soon as news is dropped in a folder, it will be processed, stock process are pulled to show the effect of news.

It will display 2 graphs - 
1) Graph that shows severity of the disruptive news 
2) Stock price of the company during that time period


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Before running this project, please make sure you have all the required python modules installed.
The software is using below python modules.
* gensim
* matplotlib
* nltk
* numpy
* pandas
* pandas_datareader
* scikit_learn
* spacy
* watchdog
* tinydb
* toml

The prerequisites are defined with respect to **Python 3**. To install python libraries, run below command:
(make sure 'requirements.txt' file is available where you are running it )

```bash
pip3 install -r requirements.txt
```

### Installing
Clone the repository and install all prerequisities.

## Usage

```python
python3 detector.py
```

## Further Improvements beyond project work
* Enhance the application to integrate with third-party News service providers like Webhose.io, Dataminr and newsapi.org  to collect news in real-time 
* Improve the logic to derive Severity using topic content changes (analysis within the text)
* Predict the stock fluctuation using topic content changes
* Use Hierarchical Dirichlet Process (HDP) to learn the number of topics and input that number to LDA instead of a fixed number of topics
* Use the Topic model to uncover emerging/new topics in time series.
* Reduce the number of dependent libraries

## References
[LDA-Based Topic Strength Analysis](https://cai.type.sk/content/2017/6/lda-based-topic-strength-analysis/)

[Exploring Topic Modelling with Gensim ](https://medium.com/@oyewusiwuraola/exploring-topic-modelling-with-gensim-on-the-essential-science-indicators-journals-list-1dc4d9f96d9c)

[Hierarchical Dirichlet Process](https://radimrehurek.com/gensim/models/hdpmodel.html)
