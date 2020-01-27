# NSFW Classifier
> Bulk checks multiple images if they are NSFW or SFW.

This small python script checks a directory of images and checks them one by one and determines if it is NSFW or SFW. It then moves the image to either a NSFW or SFW folder.
## Prerequisites

- Python 3.6.7 (Windows must use 64 bit version)
- [nsfw_model](https://github.com/gantman/nsfw_model) (Included as submodule in repo.)
- [Training Model](https://s3.amazonaws.com/ir_public/nsfwjscdn/nsfw_mobilenet2.224x224.h5) (Place in same directory as `main.py`)
## Installation
```shell script
git clone --recursive https://github.com/mclarence/nsfw_classifier
cd nsfw_classifier/nsfw_model
python setup.py install
cd ..
pip install -r requirements.txt
```
On windows, pip may fail building a `wrapt`. If this is the case use command prompt and run `set WRAPT_INSTALL_EXTENSIONS=false` before running `pip install -r requirements.txt` again.
## Usage
```shell script
usage: NsfwClassifier.py [-h] -d DIRS [DIRS ...] [--delete-sfw] [--delete-nsfw]
               [--delete-other]

Classify potential NSFW or SFW images.

optional arguments:
  -h, --help            show this help message and exit
  -d DIRS [DIRS ...], --dirs DIRS [DIRS ...]
                        <Required> The directories of images to check.
  --delete-sfw          Deletes SFW images.
  --delete-nsfw         Deletes nsfw images.
  --delete-other        Deletes non-image files.
```
Specify directories of images to check in the ```--dirs``` argument. Other arguments are self explanatory.

You can also run InteractiveMode.py for an interactive menu to run the application.