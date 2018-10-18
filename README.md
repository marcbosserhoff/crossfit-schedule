# crossfit-schedule
Generate WOD schedule for crossfit cologne

This is simple generating tool for an ICS file for the special WOD repitition scheme of the coaches of CrossFit Cologne.

Everything is explained on the command line, when you start the tool. Basic information about the workouts has to be
entered in the dictionary file 'workouts.yml'. Every 'contents' block is for one day in the schedule and should be exact
7 items. According to the scheme they will be rotated backwards througt the weeks. So the workout on Tuesday is the workout
for monday on the next week.

The calendar tool can be used for any period of time, according how long the coach plannes the training for you.
