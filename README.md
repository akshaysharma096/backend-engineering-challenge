# Bakckend Engineering Challenge


Welcome to our Engineering Challenge repository 🖖

If you found this repository it probably means that you are participating in our recruitment process. Thank you for your time and energy. If that's not the case please take a look at our [openings](https://unbabel.com/careers/) and apply!

Please fork this repo before you start working on the challenge, read it careful and take your time and think about the solution. Also, please fork this repository because we will evaluate the code on the fork.

This is an opportunity for us both to work together and get to know each other in a more technical way. If have some doubt please open and issue and we'll reach out to help.

Good luck!

## Challenge Scenario

At Unbabel we deal we a lot of translation data. One of the metrics we use for our clients' SLAs is the delivery time of a translation. 

In the context of this problem, and to keep things simple, our translation flow is going to be modeled as only one event.

### *translation_delivered*

Example:

```json
{
	"timestamp": "2018-12-26 18:12:19.903159",
	"translation_id": "5aa5b2f39f7254a75aa4",
	"source_language": "en",
	"target_language": "fr",
	"client_name": "easyjet",
	"event_name": "translation_delivered",
	"duration": 20,
	"nr_words": 100
}
```

## Challenge Objective

Your mission is to build a simple command line application that parses a stream of events and produces an aggregated output. In this case, we're instered in calculating, for every minute, a moving average of the translation delivery time for the last X minutes.

If we want to count, for each minute, the moving average delivery time of all translations for the past 10 minutes we would call your application like (feel free to name it anything you like!).

	unbabel_cli --input_file events.json --window_size 10
	
The input file format would be something like:

	{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}
	{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}
	{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 100, "duration": 54}


The output file would be something in the following format.

```
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```

#### Akshay's Notes

The problem has been solved by building it as a production ready software.

The solution is built around the queueing mechanism of adding an removing events.


- The problem is a sliding window problem, which can be solved in the most simplest way using a queue.
- My approach uses an internal queue to keep track of the number of events happened per minute and the total duration of those events, for the window of X minutes.
-  The size of the internal queue signifies the window size.
- To simplify more, I have started with grouping the events based on the basis of the minute timestamp(epoch time) they occurred.
    - Once we group them, it becomes very simple to architect the solution using a queue.
- The queueing mechanism allows use to remove the dependency to cycle over the events again and again, thus our code runs fast.
- The code has been made modular by methods to carry out small tasks, this makes it easy to read as well as easily debuggable.
- The code runs with a runtime complexity of *O(n)*, where *n* is the number of events passed in the source file.
- The code has a space complexity of *O(n)* also, as we internally group the events using the minute timestamp.


##### Additional cases
- An important edge is to consider is the case, where window size is 1. 
- Another important edge case to remove those events whose *event_name* is not part of what the problem has asked, i.e *translation_delivered*.
- Handle bad timestamps, the application should stop if input data is wrongly formatted.
- Handling files with invalid formatting has been handled, or non JSON files.
- If any of the keys, *event_name* or *duration* does not exist in the event, it should be skipped.
   
#### How to run
- The code has been written using Python3.6

- You can run the command line app using the command.

```buildoutcfg
python3 moving_average.py -i input.json -w 20 -o result.json
```


#### Notes

Before jumping right into implementation we advise you to think about the solution first. We will evaluate, not only if your solution works but also the following aspects:

+ Simple and easy to read code. Remember that [simple is not easy](https://www.infoq.com/presentations/Simple-Made-Easy)
+ Include a README.md that briefly describes how to build and run your code
+ Be consistent in your code. 

Feel free to, in your solution, include some your considerations while doing this challenge. We want you to solve this challenge in the language you feel most confortable with. Our machines run Python, Ruby, Scala, Java, Clojure, Elixir and Nodejs. If you are thinking of using any other programming language please reach out to us first 🙏.

Also if you have any problem please **open an issue**. 

Good luck and may the force be with you

#### Extra points

If you feeling creative feel free to consider any additional cases you might find interesting. Remember this is a bonus, focus on delivering the solution first.

