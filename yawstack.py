##### Yawstack ####
# Yawcam companion script to automatically retrieve, noise-reduce, and archive images
# cpf@cpfx.ca
# Jan 7 2013

#### Config Defaults ####
## General ##
# see http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
ArchivePath = "archive/%H-%M-%S_%d-%m-%Y.jpg"
# unless you change the HTTP publish settings, don't change this
YawcamURL = "http://127.0.0.1:8888/out.jpg"
# how often (secs) to capture and archive an image (time taken to stack images is accounted for)
CaptureInterval = 60
## Stacking ##
# number of images to stack (law of diminishing return applies)
StackDepth = 10
# timespan (secs) between capturing images to be stacked
StackInterval = 0.25
## Output ##
# dump lots of records to stdout
Verbose = False
# warns when captures aren't running fast enough to achieve CaptureInterval
WarnMissedInterval = False
# warns when images aren't being captured fast enough to achieve StackInterval.
WarnMissedIntersitialInterval = False


#### Code starts here ####
import argparse
import os
import urllib2
import datetime
import time
import subprocess

LastCaptureTimestamp = datetime.datetime.min

argParser = argparse.ArgumentParser(description="Yawcam companion script to automatically retrieve, noise-reduce, and archive images. Best results if Yawcam is set to output full-quality JPEGs at maximum resolution.", epilog="IMPORTANT NOTE: ImageStack.exe must be in same directory as yawstack.py")
argParser.add_argument("--archive", help="Image archive path pattern (default " + ArchivePath.replace("%", "%%") + ")", default=ArchivePath, metavar="PATH")
argParser.add_argument("--image-url", help="Webcam image URL (default " + YawcamURL + " aka 'HTTP Output')", default=YawcamURL, metavar="URL")
argParser.add_argument("--interval", help="Archive interval (seconds, default " + str(CaptureInterval) + ")", default=CaptureInterval, metavar="SECS", type=float)
argParser.add_argument("--stack-depth", help="Number of images to stack (default " + str(StackDepth) + ")", default=StackDepth, metavar="COUNT", type=int)
argParser.add_argument("--stack-interval", help="Interval between consecutive images in stack (secs, default " + str(StackInterval) + ")", default=StackInterval, metavar="SECS", type=float)
argParser.add_argument("--verbose", help="Dump lots of logging to stdout", action="store_true", default=False)

args = argParser.parse_args()
Verbose = args.verbose
ArchivePath = args.archive
YawcamURL = args.image_url
CaptureInterval = args.interval
StackInterval = args.stack_interval
StackDepth = args.stack_depth


def verbosePrint(*args):
    if Verbose == True:
        print "".join(str(x) for x in args)


def capture():
    captureStartedTimestamp = datetime.datetime.now()
    lastImageTimestamp = datetime.datetime.min
    # prep
    if not os.path.exists("temp/"):
        os.makedirs("temp/")

    for i in range(StackDepth):
        if WarnMissedIntersitialInterval and ((datetime.datetime.now()) - lastImageTimestamp).total_seconds() < StackInterval:
            print("WARNING: StackInterval too small - not actually a problem unless you care that pre-stack images are being captured at exact intervals")

        # wait until ts has elapsed
        while ((datetime.datetime.now()) - lastImageTimestamp).total_seconds() < StackInterval:
            time.sleep(0.01)

        #capture from yawcam output
        lastImageTimestamp = datetime.datetime.now()
        verbosePrint("Beginning capture of image ", i, " at ", lastImageTimestamp)
        img = urllib2.urlopen(YawcamURL)
        output = open("temp/" + str(i) + ".jpg", "wb")
        output.write(img.read())
        output.close()

    # stack
    verbosePrint("Beginning stack at ", datetime.datetime.now())
    stackParams = [os.path.dirname(__file__) + "/ImageStack.exe"]
    stackParams.extend('-load "temp/' + str(i) + '.jpg"' + ("" if i == 0 else " -add") for i in range(StackDepth))
    stackParams.append("-scale " + str(1.0 / StackDepth))  # average

    outputPath = captureStartedTimestamp.strftime(ArchivePath)
    if not os.path.exists(os.path.dirname(outputPath)):
        os.makedirs(os.path.dirname(outputPath))

    stackParams.append('-save "' + outputPath + '" 90')  # number is jpeg quality

    subprocess.call(" ".join(stackParams), stdout=subprocess.PIPE)

    print "Capture + stack completed at ", str(datetime.datetime.now())

while True:
    if WarnMissedIntersitialInterval and ((datetime.datetime.now()) - LastCaptureTimestamp).total_seconds() < CaptureInterval:
            print("WARNING: CaptureInterval too small - not actually a problem unless you care that images are being arcnived at exact intervals")
    # wait for ts to elapse
    while (datetime.datetime.now() - LastCaptureTimestamp).total_seconds() < CaptureInterval:
        time.sleep(0.1)
    LastCaptureTimestamp = datetime.datetime.now()
    capture()
    print "Next capture will occur in ", round(CaptureInterval - (datetime.datetime.now() - LastCaptureTimestamp).total_seconds()), " secs"
