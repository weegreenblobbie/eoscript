Eclipse Orchestdrator Scripting
===============================

This is a simple python script that makes generating a CSV file to be loaded
into Eclipse Orchestrator (EO) program by
[Moonglow Technologies](http://www.moonglowtechnologies.com/products/EclipseOrchestrator/index.shtml).

How to write your own scipt
===========================

Clone this repo, install `requirements.txt` into a python virtual enviornment,
then run the script:

    python main.py

This will generate the named CSV file that you can load into Eclipse Orchestrator.
You can verify correctness by **File** -> **View Exposure Sequence** which will dump a time orderd list of the
exposures you've configured with your scirpt.

Be sure test your setup by choosing **Location/Time** -> **Simulated Second Contact** and verify:
* The number of image captured.
* The captured images have the corret ISO and shutter speeds.

You can run a simulation, then pop your camera's memory card into a card reader and scan the path with `scan_photos.py`:

    python scan_photos.py d:\DCIM\102NZ7__\
    Filename                        , Offset       , Campera, Exposure, Fstop, ISO, Quality
    d:\DCIM\102NZ7__\_NIK2589.NEF   , +,00:00:00.0, NIKON Z 7, 1/8000, 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2590.NEF   , +,00:00:02.8, NIKON Z 7, 1/4000, 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2591.NEF   , +,00:00:05.7, NIKON Z 7, 1/2000, 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2592.NEF   , +,00:00:08.8, NIKON Z 7, 1/1000, 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2593.NEF   , +,00:00:11.8, NIKON Z 7, 1/500 , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2594.NEF   , +,00:00:14.7, NIKON Z 7, 1/250 , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2595.NEF   , +,00:00:17.7, NIKON Z 7, 1/125 , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2596.NEF   , +,00:00:20.7, NIKON Z 7, 1/60  , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2597.NEF   , +,00:00:23.8, NIKON Z 7, 1/30  , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2598.NEF   , +,00:00:26.8, NIKON Z 7, 1/15  , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2599.NEF   , +,00:00:29.7, NIKON Z 7, 1/8   , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2600.NEF   , +,00:00:32.8, NIKON Z 7, 1/4   , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2601.NEF   , +,00:00:35.9, NIKON Z 7, 1/2   , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2602.NEF   , +,00:00:38.9, NIKON Z 7, 1     , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2603.NEF   , +,00:00:41.9, NIKON Z 7, 2     , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2604.NEF   , +,00:00:44.9, NIKON Z 7, 4     , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2605.NEF   , +,00:00:57.6, NIKON Z 7, 15    , 8   , 64  , RAW
    d:\DCIM\102NZ7__\_NIK2606.NEF   , +,00:01:44.6, NIKON Z 7, 30    , 8   , 64  , RAW

If you're missing photos:
* Use a USB to serial cable wired up to your camera's shutter release port.  The USB interface isn't fast enough to
trigger many exposures back to back.
* Add timing delay between exposures by setting up a larger `minimum_time_step`.

