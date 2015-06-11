
Welcome to the crash-stats-bugzilla wiki! This is a multi-script project that will eventually morph its way into something bigger and better.

**So what's in it for me?**
Good question. I'll explain each of the current scripts. 
  1. CheckTopCrash.py is a script designed to return 39+ bugs with crash signatures and their crash rankings for each version. It is currently working with data export going to the command line, a text file, and a CSV.

  2.  CrashExplore.py is currently retrieving a list of 39+ bugs with crash signatures and returning information about those bugs. It isn't currently working properly because of conversion from Python strings into URL-friendly encoding. Also, the data it is returning isn't analyzed or parsed and comes out as a giant JSON blob.

  3.  Ah, got you! There is no actual program for grabbing and sentiment analyzing user comments, but there will be! It is one of my personal goals for this project.

**So how do I run this stuff?**
Sorry, I didn't include a VENV. You need to have Python 2.7.6. and download all of the modules that I am using. Don't worry, you won't regret it! They are all pretty basic and useful modules.
