yawstack
========

Yawcam companion script to automatically retrieve, noise-reduce, and archive webcam images. A series of images are downloaded from a specified URL (usually Yawcam's Http Output option), then averaged together to produce a noise-reduced image which is then archived.

Tested on **Python 2.7 + Yawcam 0.3.9 + ImageStack 2010-7-31-win32 + Windows 7 x64**. 

Instructions
------------
0. Download ImageStack.exe from [http://code.google.com/p/imagestack/](http://code.google.com/p/imagestack/) and place it in the same directory as `yawstack.py`
0. Enable HTTP output in Yawcam
0. Steps after this point are optional but recommended
0. Max out webcam resolution (In Yawcam, Settings→Device xxxx→Device properties)
0. Max out HTTP publish JPEG quality (In Yawcam, Settings→Edit Settings→Output/Http→Image quality)

Scheduling
----------
yawstack has a built-in automatic capture feature: `--interval time_in_seconds`. The additional `--interval-snap` option will align captures to clean wallclock times. That is, with a 5 minute capture interval and `--interval-snap`, images would be captured at 12:35:00, 12:40:00, etc. instead of 12:33:15, 12:38:15, etc.

*That said,* for ultimate long-term stability I recommend using cron/Task Scheduler to make sure logging isn't derailed by an undiscovered bug in this script. Unlikely, but possible.

Usage
-----
	usage: yawstack.py [-h] [--output PATH] [--image-url URL] [--interval SECS]
                   [--interval-snap] [--stack-depth COUNT]
                   [--stack-interval SECS] [--verbose]

	Yawcam companion script to automatically retrieve, noise-reduce, and archive
	images. Best results if Yawcam is set to output full-quality JPEGs at maximum
	resolution.

	optional arguments:
	  -h, --help            show this help message and exit
	  --output PATH         Image output path pattern (default
	                        archive/%H-%M-%S_%d-%m-%Y.jpg)
	  --image-url URL       Webcam image URL (default
	                        http://127.0.0.1:8888/out.jpg aka 'HTTP Output')
	  --interval SECS       Archive interval (seconds, default 0 = one-off)
	  --interval-snap       Align captures with wall-clock times
	  --stack-depth COUNT   Number of images to stack (default 10)
	  --stack-interval SECS
	                        Interval between consecutive images in stack (secs,
	                        default 0.25)
	  --verbose             Dump lots of logging to stdout

	IMPORTANT NOTE: ImageStack.exe must be in same directory as yawstack.py