# Visualising the Formula 1 2022 Calendar

## Welcome  

Whether you consider yourself a true Formula 1 veteran, or this is the first time you've heard of the sport, we bid you welcome to: [our dashboard!](https://f1-2022.onrender.com/)  

Firstly, a quick overview of what you can find on this page:
- [Visualising the Formula 1 2022 Calendar](#visualising-the-formula-1-2022-calendar)
  - [Welcome](#welcome)
  - [The Contributors](#the-contributors)
  - [The Motivation](#the-motivation)
  - [The Need-to-Know](#the-need-to-know)
  - [The Description](#the-description)
  - [The Contributing Guidelines](#the-contributing-guidelines)
  - [The License](#the-license)
  - [The Credits](#the-credits)

![Lights out](/www/sketch/lights_out.png)

## The Contributors

I am a student at UBC, Vancouver, part of the Master of Data Science program:

- [Renzo Wijngaarden](https://github.com/RenzoWijn)

## The Motivation

Formula 1 is the pinnacle of motorsport, and the circus and its entourage travels across 5 different continents throughout one season. It can get difficult to keep track of where the next race is, and how that race compares to the one from previous weekend. My dashboard looks to provide a quick, interactive summary of the 2023 calendar, so one can look at track statistics and the route Formula 1 is taking.

## The Need-to-Know

Of course not everyone is as familiar with Formula 1 as the most dedicated fan, so here is a super quick run down to get you up to speed:

The Formula 1 season runs from the start to the end of the calender year, with the first race usually taking place around March, and the last one around December. In one season, 20 drivers spread out over 10 teams try and accumulate as many points as possible. Any point they score counts towards two different competitions: the Drivers Championship  and the Constructors Championship. This means that the driver that has the most points after the last race is World Champion, and the two drivers that race for the same team who have the most total points combined, make their team the Constructors Champion.

So how does one get these points? Each weekend, the drivers get three practice sessions, after which they continue to qualifying. During qualifying they have to try and drive as fast as possible for one single lap. Then, the order of who drove the fastest lap determines the starting grid for the race on Sunday.  

On race day, the drivers race for 300 kilometers around that weekends track, in a spectacle that isn't just about who can drive the fastest, but also about what cars have the best design, what team can deliver the fastest pitstops, and what driver manages to stay out of collisions.

Then, once the 300 kilometers are up, the order in which the drivers cross the finish line determines their position for that race, and more importantly how many points they get! And additionally, the driver that set the fastest lap time during the race, receives one extra bonus championship point.

## The Description

![Dashboard](/reports/Dashboard.png)

Our app opens on the Season Calendar page. On the left hand side you can see all the details of the selected track, including a map of its layout. To the right is the world map, with all the locations of the races for this years calendar. When you click one, its details will show up in the table to the left. There is also a toggle button to display the order and the route in which this season takes place, to understand where the next race is in comparison with the current!

## The Contributing Guidelines
Do you have ideas on how I can improve my dashboard, and are you interested in contributing? I'd love to see your suggestions! To make changes locally just clone the repo, navigate to the top folder, and run the app:

```
git clone git@github.com:RenzoWijn/f1-2023-calendar.git # If SSH is set up

cd f1-2023-calendar

python app.py
```

Check out the [contributing guidelines](CONTRIBUTING.md) if you're looking to make additions to our project! Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By contributing to this project, you agree to abide by its terms.
## The License
`f1-2023-calendar` was created by Renzo Wijngaarden. It is licensed under the terms of the MIT license.
## The Credits
The datasets used in this app are from [Formula 1 World Championship (1950 - 2022)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020?select=lap_times.csv) on Kaggle and from [Formula 1 Datasets](https://github.com/toUpperCase78/formula1-datasets) on Github. The track images are from [the Formula 1 website](https://www.formula1.com/en/racing/2023.html).