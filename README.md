# :muscle: `workout` - Exercise App

Application to run and time workout routines.

Features:

- Pause and resume the timer
- Customize the workout routine (read [below](#customize-workouts))
- Rest period between exercises
- Stop exercise button to return to the welcome screen
- Resets to the welcome screen after the last exercise

This application was created in a couple of hours using the `pygame-ce` package for personal use.

## Installation

Download or clone the repository to your local machine:

```shell
git clone https://github.com/nachomaiz/nyt-workouts.git
```

Go to the newly created repository folder on your terminal and create and activate a virtual environment:

```shell
cd nyt-workouts
python -m venv venv
venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the package:

```shell
pip install .
```

Now you can run the application:

```shell
python -m workouts
```

## Workouts

Currently the existing workout is the [New York Times's *Well Workouts* "Scientific 7-Minute Workout"](https://archive.nytimes.com/well.blogs.nytimes.com/2013/05/09/the-scientific-7-minute-workout/).

## Customize workouts

Workouts are read from the `assets/data/workout_data.json` file. Change the routine or create your own by modifying that file.

> [!WARNING]
> If you want to keep the original workout file, make sure to make a backup!

```json
[
    {
        "title": "My Exercise 1",
        "duration": 60.0,  // in seconds, optional [default is 30.0]
        "rest_duration": 5.0  // in seconds, optional [default is 10.0]
    },
    // ...
]
```
