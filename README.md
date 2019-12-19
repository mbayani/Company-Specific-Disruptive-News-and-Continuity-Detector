# Disruptive News Detector

In this project, we built a software to detect company-specific disruptive news and continuity of news from news articles in real-time and present the right discontinuity and severity information to the user.
It then further analyze the disruptive news to check its affect on the stock price of that company. 
It will display 2 graphs - 
1) Graph that shows severity of the disruptive news 
2) Stock price of the company for that time period

It reads news to detect any disruptive news about a company.
There are 2 modes to run it (driven by settings)- 1) Batch Mode and 2) Continous Monitoring

1) Batch Mode - It reads already stored news from a folder and process them. It shows on graph the disruptive news
    severity. Along with it, it pulls the stock price for that company during that time period. Trying to depict
    the affect of disruptive news on its stock price.

2) Continous Monitoring - We can run the program to process live news feed. As soon as news is dropped in a folder,
    it will be processed, stock process are pulled to show the affect of news.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Before running this project, please make sure you have all the required python modules installed.
It has Python 3.x dependency defined. To install python libraries, run below command:
(make sure 'requirements.txt' file is available where you are running it )

pip3 install -r requirements.txt


```
Give examples
```

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
