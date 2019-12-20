# Disruptive News Detector

Disruptive/Negative news coverage, such as poor earnings reports or stories of bad corporate governance, normally decrease demand, meaning more people want to sell the stock, thereby lowering the market price. Demand can also be negatively affected by news stories covering economic and political uncertainty, or unexpected, negative events.

In this project, we built a software to detect company-specific disruptive news and continuity of news from news articles in real-time and present the right discontinuity and severity information to the user. The software processes the news articles and predicts whether it is disruptive for the company, which is mentioned in the news article or not. It then further fetches the stock price of the company in real-time and try to show the coorelation between the negative news and stock price fluctuations. 

There are 2 modes to run it (driven by settings)- 1) Batch Mode and 2) Continous Monitoring

1) Batch Mode - In this mode, some news are already copied in the input folder. Program process each news one-by-one and determines if news is negative for a company or not and what is the severity level. It shows the news severity on graph. Along with it, it pulls the stock price of that company during that time period. Trying to show the coorelation between news and its stock price.

2) Continous Monitoring - We can run the program to process live news feed. Program will monito for any new news dropped in an input folder. As soon as news is dropped in a folder, it will be processed, stock process are pulled to show the effect of news.

It will display 2 graphs - 
1) Graph that shows severity of the disruptive news 
2) Stock price of the company during that time period


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Before running this project, please make sure you have all the required python modules installed.

The software needs below python 3.x modules:
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

The prerequisites are defined with respect to Python 3.x. To install python libraries, run below command:
(make sure 'requirements.txt' file is available where you are running it )

pip3 install -r requirements.txt


### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
