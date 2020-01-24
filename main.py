import os
import configparser
import shutil
import argparse
import logging

parser = argparse.ArgumentParser(description="Classify potential NSFW or SFW images.")
parser.add_argument('-d', '--dirs', nargs='+', help='<Required> The directories of images to check.', required=True)
parser.add_argument('--delete-sfw', help='Deletes SFW images.', action='store_true')
parser.add_argument('--delete-nsfw', help='Deletes nsfw images.', action='store_true')
parser.add_argument('--delete-other', help='Deletes non-image files.', action='store_true')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s [%(levelname)8s] - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

invalid_directories = []
for directory in args.dirs:
    if not os.path.isdir(directory):
        logging.error(str.format("{} does not exist or is not a directory!", directory))
        invalid_directories.append(directory)

if len(invalid_directories) is not 0:
    logging.critical("The application encountered a fatal error. Will now exit!")
    exit(1)



logging.info("Loading model...")
from nsfw_detector import NSFWDetector
detector = NSFWDetector('./nsfw_mobilenet2.224x224.h5')
logging.info("Model loaded!")
dircount = len(args.dirs)
processed_dir = 1
for dir in args.dirs:
    files = os.listdir(dir)
    if not os.path.isdir(os.path.join(dir, "nsfw")) and not args.delete_nsfw:
        os.makedirs(os.path.join(dir, "nsfw"))
    if not os.path.isdir(os.path.join(dir, "sfw")) and not args.delete_sfw:
        os.makedirs(os.path.join(dir, "sfw"))
    filecount = len(files)
    processed = 0
    nsfw_count = 0
    sfw_count = 0
    for file in files:
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            logging.info(str.format("Checking {}", file))
            fullpath = os.path.join(dir, file)
            results = detector.predict(fullpath, image_size=(224, 224))
            if results[fullpath]['neutral'] <= 0.50 and (results[fullpath]['sexy'] >= 0.40 or results[fullpath]['porn']
                                                         >= 0.40 or results[fullpath]['hentai'] >= 0.50):
                logging.info(file + " is nsfw.")
                if not args.delete_nsfw:
                    shutil.move(os.path.join(dir, file), os.path.join(dir, str.format("{}/{}", 'nsfw', file)))
                else:
                    os.remove(fullpath)
                    logging.info("Deleting " + fullpath)
                nsfw_count += 1
            else:
                logging.info(file + " is sfw.")
                if not args.delete_sfw:
                    shutil.move(os.path.join(dir, file), os.path.join(dir, str.format("{}/{}", 'sfw', file)))
                else:
                    os.remove(fullpath)
                    logging.info("Deleting " + fullpath)
                sfw_count += 1
        elif args.delete_other and not os.path.isdir(os.path.join(dir, file)):
            os.remove(os.path.join(dir, file))
            logging.info("Deleted " + file)

        processed += 1
        logging.info(str.format("[Directory ({}/{}): {}] [Processed: {}/{}] [NSFW: {}] [SFW: {}]", str(processed_dir),
                                str(dircount), str(os.path.basename(dir)), str(processed), str(filecount),
                                str(nsfw_count),
                                str(sfw_count)))
    processed_dir += 1

logging.info("Done!")
