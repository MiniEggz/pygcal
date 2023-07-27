# pygcal
CLI tool to interact with google calendar api.

# Usage

Currently this application only supports viewing the next x calendar events and recording events based on a timer.

## View
To view the next x calendar events,
```
pygcal view -n x
```
The default value of x is 10, so 
```
pygcal view
```
will show the next 10 events at most.

## Timer
Timing events with the CLI is for tracking daily activities with google calendar. You are able to start an event and stop an event. On stopping the event, you add the event to your calendar.

### Start
To start a timer event, simply run the command:
```
pygcal start event_name
```

If you want to add a description to your event:
```
pygcal start event_name -d "Your description"
```

### Stop
After you have finished doing what you are doing, you can stop the event using the command:
```
pygcal stop event_name
```

After stopping this, you should be able to see the event in your calendar.

# Installation

TODO.
