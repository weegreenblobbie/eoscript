Eclipse Orchestdrator Scripting
===============================

This is a simple python script that makes generating a CSV file to be loaded
into Eclipse Orchestrator (EO) program by
[Moonglow Technologies](http://www.moonglowtechnologies.com/products/EclipseOrchestrator/index.shtml).

How to write your own scipt
===========================

Clone this repo, install `requirements.txt` into a python virtual enviornment,
then run the script:

    python eoscript.py

This will generate the named CSV file that you can load into Eclipse Orchestrator.
You can verify correctness by **File** -> **View Exposure Sequence** which will dump a time orderd list of the
exposures you've configured with your scirpt.

Be sure test your setup by choosing **Location/Time** -> **Simulated Second Contact** and verify:
* The number of image captured.
* The captured images have the corret ISO and shutter speeds.

If you're missing photos:
* Use a USB to serial cable wired up to your camera's shutter release port.  The USB interface isn't fast enough to
trigger many exposures back to back.
* Add timing delay between exposures by setting up a larger `minimum_time_step`.

