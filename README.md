<img src="https://app.peelinsights.com/cdn/img/peel_black.svg" width=200>

# Peel Challenge - Resolution
The following lines will be elaborate on the solution for the challenge

## Architectural Functional viewpoint
The functional requirements are simple: allow an API client to compare two datasets and obtain includes only rows that are guarantee to have different values or new ones.
It's only required to have an API service, working along with a background worker that will process the heavy tasks (the file processing). Below a functional representation of the components involved.
![Alt text](peel-api_functional-view.png?raw=true "Functional diagram")

## Technical overview
For the resolution, was reused the base Django application offered as the guideline for this challenge. The database implementation remains the same, works just fine for the purpose. 
It was integrated the use of celery and redis to handle the background tasks.
Besides, the application was dockerized in order to easily be distributed and for the sake of the challenge review. 

## Challenge conclusions
- The solution implemented for the diffing process is a "naive" solution, that certainly can be improved.
- Since the solution is considered "production-ready", was preferred to be dockerized, easing the process of running the application, even better, to ship it out using a service such as AWS ECS fargate.
- Time of execution: revenue metric: 72.319462348s, c_revenue metric: 459.116917938s
- The way this was implemented, the time increments exponentially the number of rows in the dataset. Some other better approaches may be explored:
    * Explore pandas and its API in order to find a better way, there should be a recipe for this kind of scenario.
    * Implement a solution based on map reduce, guaranteeing the data sets will be handle as segmented chunks, improved the way those are processed.
- Personal philosophy followed in development: 'Make it once, then make it better, and finally scale it'.
- During the development was preferred to follow the provided project skeleton, developing clean and readable code, focusing on the easing of delivering it to production-ready state and fulfilling the core challenge: the diffing process.
- Unit test included to test the core functionality: the diffing process.


## Environment setup
The project uses pipenv for declaring Python dependencies and is set to use Python 3.8 and Django 2.2.

### Previous requirements
- It's required to download the proper datasets `c_revenue_new.csv`, `c_revenue_old.csv`, `revenue_new.csv`, `revenue_old.csv` and place them into the folder ./diffing/assets/input. Otherwise, the application won't be able to read those files and processing the requests.
- Python 3.8
- Django 2.2
- Docker >= 19.03.8
- Docker-compose >= 1.25.4

### Preparing the Python env
- `pipenv --python 3.8 shell` 
- `pipenv install -d`

### Running tests
Test was included to verify the core diffing functionality, run in terminal
```sh
python manage.py test
```

### Running using docker-compose
If you want to avoid all the hard work of executing all the commands and having the requirements installed, it's only required to have Docker and docker-compose and rely on them.
For the sake of simplicity, you can reuse the makefile included.

#### Start the application 
- Run in terminal
```sh
make up
```
That's everything you need to have your application running, it will prepare and start the following services: API, redis and the celery worker.
From now the application can be accessed by http://localhost:8000 (Scroll down to check the actual API documentation and endpoints)

If you prefer to do it by using vanilla docker-compose, run in terminal
```sh
docker-compose up -d
```
#### Stopping the application
- Run in terminal
```sh
make down
```

Docker-compose vanilla option:
```sh
docker-compose down -v
```

#### Accesing logs
- Run in terminal
```sh
make logs
```

Docker-compose vanilla option:
```sh
docker-compose logs -f
```

### Running the application - manual way
If you still want to run the applications piece by piece, here are the steps.

#### Start the application 
The preference is to have 3 terminal open. 
- 1st terminal for redis, which is dockerized, run:
```sh
make redis_svc
```
- 2nd terminal for the API, run:
```sh
$ python manage.py migrate
$ python manage.py runserver
```

- 3rd terminal for celery, run:
```sh
celery  -A platform_challenge worker -l info
```

At this point you should be able to access the endpoints in http://localhost:8000 (Scroll down to check the actual API documentation and endpoints)

---

## Instruction for completing and submitting the challenge:

Thanks for applying to Peel! 
Welcome to our coding challenge for the platform role, this is a space for you to share with us how you work and reason about the problem presented, what things you care about when doing coding work, and how you approach problem solving. As such, through this challenge we are not expecting to check if you know the finest algorithms, have all the right answers to a given situation or if you are the best coder in the world. We believe there are no right or wrong answers, so please make yourself comfortable and focus on what you know best.

Luckily we have done some work before hand of setting up this project with the default Django template, so you can focus on the actual solution.

**Please submit your ideas to us in 1 week (max).** This will give us enough time to review your challenge with the rest of the team before the next interview. During this interview we will take some time to explore together your coding challenge submission, and will ask you any clarifying questions we might have.

Based on previous candidate experiences, we believe **it will take you between 10 and 12 hours to complete the challenge.** 

## Objective

Most times at Peel our platform has to run operations on big datasets that need to be handled fast and optimized to use a minimal memory and CPU footprint, you are tasked to build a task that can do a diff of two given datasets and return the results in an API.


### Datasets

Since Peel supports many different metrics, diffing can change depending on the important keys on each metrics, for the sake of this challenge you will only work with `cohort-revenue` and `revenue`. Another important fact of Peel is that all metrics can be segmented so you need to guarantee the diffing handles correctly values with or without a segment.

For `c-revenue` the unique keys are `cohort`,`cohort_id`,`month_nth`,`[segment_field]`,`[segment_value_id]` and `stat`.
For `revenue` the unique keys are `date`, `[segment_field[`, `[segment_value_id]` and `stat`.

We will make sure to give you CSV datasets for testing for both metrics by email when receiving this challenge. See below for a teaser of how a dataset would look

```
cohort,cohort_id,month_date,month_nth,segment_field,segment_name,segment_value,segment_value_id,stat,value
2015-07-01,15,2015-07-01,,,,,,c-revenue-pc,75.12679951100245
2015-07-01,15,2015-08-01,1,,,,,c-revenue,312241.31
2015-07-01,15,2015-08-01,1,,,,,c-revenue-pc,76.34261858190709
2015-07-01,15,2015-09-01,2,,,,,c-revenue,328424.91
2017-10-01,15,2020-04-01,30,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,136.4535643564356
2017-10-01,15,2020-05-01,31,shipping_province,states,Western Australia,Western Australia,c-revenue,13781.809999999998
2017-10-01,15,2020-05-01,31,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,136.4535643564356
2017-10-01,15,2020-06-01,32,shipping_province,states,Western Australia,Western Australia,c-revenue,13781.809999999998
2017-10-01,15,2020-06-01,32,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,136.4535643564356
2017-10-01,15,2020-07-01,33,shipping_province,states,Western Australia,Western Australia,c-revenue,13781.809999999998
2017-10-01,15,2020-07-01,33,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,136.4535643564356
2017-10-01,15,2020-08-01,34,shipping_province,states,Western Australia,Western Australia,c-revenue,13866.309999999998
2017-10-01,15,2020-08-01,34,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,137.29019801980195
2017-10-01,15,2020-09-01,35,shipping_province,states,Western Australia,Western Australia,c-revenue,13866.309999999998
2017-10-01,15,2020-09-01,35,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,137.29019801980195
```


### Diffing

Given two datasets a new one and an old one, you should return the new datasets that includes only rows that are guarantee to have a different values or new ones. Some values might have very small differences so we recommend using `math.isclose(new_val, old_val):  # Precision of 1e-09`. 

### APIS
`http://localhost:8000/api/diffing/new/<metric_id>`

The API should create a new job/task for running a diff for a given metric, for this challenge is safe to assume you can read the files from disc and the files are mapped for each metric. The only parameter the API reads is the ID of the metric, for example `new/revenue`.

The API should return a job id that can be used to retrieve the diff when is ready.

Response
```
{
  "job_id": 1
}
```

`http://localhost:8000/api/diffing/job/<id>`

For retrieving a CSV download of the final diff we will use this API with the job_id we got previously. In case the job has not finished the API should just return a status code 404 not found. Optionally you can return a status of the job, but you will have to keep tracked of the status while the job is executing.

```
{
  "job_id": 1
  "status": "processing"
}
```

### Async Jobs
We want you to have full flexibility here, at Peel we use `celery` and `rabbitmq` for async jobs, but feel free to use anything you are familiar with to save time, from Python's `multiprocessing` to `concurrent.futures` to `Redis Queue`.


## Technical requirements and Tips
There are a few rules that we would like you to follow during your code challenge:
  - Make sure the diffing is fast without using too much resources, please include in your readme information on how long it takes to diff and approximately how much memory it uses.
  - Feel free to do the diffing manually in pure CSV or with pandas, thou watch out for pandas memory consumption.
  - The Django template comes with a Job model and a sqlite DB, don't waste to much time on DB handling stuff, thou feel free to edit the model as it suits you. 
  - The project uses pipenv for declaring Python dependencies and is set to use Python 3.8 and Django 2.2, you can setup your environment using `pipenv --python 3.8 shell` and then `pipenv install -d`


Your submission should also include a readme file, where you can document your work, describe the features and the architectural decisions that you made. Feel free to share there your thoughts about the challenges that you faced implementing this code. Please include any specific instructions that we might need to test your solution.


## What’s next?
Once you submit your solution, our team will review your code challenge, taking your experience level into account. The sample code provided by you should be in a state considered as a "production" ready - where each requested element is prepared and potentially ready to review with your colleagues.


Good luck!

**“The Challenge” has been created with the sole intention of being used as a guiding document for the current recruitment process. This means we won't be using it (all or parts of it) within our projects.**


celery  -A platform_challenge worker -l info
docker run --name flower -p 5555:5555 mher/flower:0.9.5 flower --broker=redis://localhost:6379