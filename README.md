# Run Less, Run Faster
## Runners at all levels can improve their race times while training less -- with the revolutionary Furman Institute of Running and Science Training (FIRST) program

[FIRST Home Page](http://www2.furman.edu/sites/first/Pages/default.aspx)

This application generates a detailed training plan for runners based on the FIRST method.
It outputs a text file with the plans specifics and a training file (TCX) for Garmin sports wearables.

### Architecture
**training plan**
- name - plan name
- weekly schedule - which days of the week you run
- race - the race you are training for
- runner - you
- workouts - a list of workout

**race**
- race type
  - name - Marathon, Half Marathon, 10K, 5K
  - distance - 26.22, etc
- name - race name like San Francisco Marathon
- date
- target time - what time you want to achieve in this race
- status - scheduled, done, skipped
- actual time

**runner**
- name
- age
- gender
- email
- length unit - preferred length unit

**workout**
- name
- date
- status - scheduled, done, skipped
- steps - list of step (basic step)

**step**
two flavours derived from basic-step:
- body
- repeat

**step-body**
distance step - run a specific distance in a specific pace
time step - run a specific time in a specific pace
- pace
- intensity
- distance or time

**step-repeat**
- repeat - how many times to repeat the following list of steps
- steps - a list of steps, either body or repeat (recursively)

### Parameters

### Development
- API
- UI
- Enable replacing pace with speed
- Enable changing the plan's units:
  - length: m, km, mile, ft
  - pace: min per mile, min per km
  - speed: mile/hr, km/hr, m/s
