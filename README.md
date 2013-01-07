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


Usage
-----
	usage: yawstack.py [-h] [--archive PATH] [--image-url URL] [--interval SECS]
	                   [--stack-depth COUNT] [--stack-interval SECS] [--verbose]

	Yawcam companion script to automatically retrieve, noise-reduce, and archive
	images. Best results if Yawcam is set to output full-quality JPEGs at maximum
	resolution.

	optional arguments:
	  -h, --help            show this help message and exit
	  --archive PATH        Image archive path pattern (default
	                        archive/%H-%M-%S_%d-%m-%Y.jpg)
	  --image-url URL       Webcam image URL (default
	                        http://127.0.0.1:8888/out.jpg aka 'HTTP Output')
	  --interval SECS       Archive interval (seconds, default 60)
	  --stack-depth COUNT   Number of images to stack (default 10)
	  --stack-interval SECS
	                        Interval between consecutive images in stack (secs,
	                        default 0.25)
	  --verbose             Dump lots of logging to stdout

	IMPORTANT NOTE: ImageStack.exe must be in same directory as yawstack.py

