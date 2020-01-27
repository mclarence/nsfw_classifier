import os
import shutil
import argparse
import configparser
import logging
import time

def main(raw_args=None):
    parser = argparse.ArgumentParser(description="Classify potential NSFW or SFW images.")
    parser.add_argument('-d', '--dirs', nargs='+', help='<Required> The directories of images to check.', required=True)
    parser.add_argument('--delete-sfw', help='Deletes SFW images.', action='store_true')
    parser.add_argument('--delete-nsfw', help='Deletes nsfw images.', action='store_true')
    parser.add_argument('--delete-other', help='Deletes non-image files.', action='store_true')
    parser.add_argument('--same-dir', help='Do not move files into a nsfw or sfw directory, Requires --delete-sfw or '
                                           '--delete-nsfw.', action='store_true')
    args = parser.parse_args(raw_args)
    if args.same_dir and not (args.delete_sfw or args.delete_nsfw):
        print("'--delete-nsfw' or '--delete-sfw' required when using '--same-dir'")
        exit(1)
    if args.delete_nsfw and args.delete_sfw:
        print("Using '--delete-sfw' and '--delete-nsfw' deletes everything.")
        exit(1)
    config = configparser.ConfigParser()
    if not os.path.isfile("./config.ini"):
        logging.debug("Creating config file.")
        config['DEFAULT'] = {
            'neutral_percentage': 0.50,
            'sexy_percentage': 0.40,
            'porn_percentage': 0.50,
            'hentai_percentage': 0.50,
            'log_level': 'DEBUG'
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    config.read('config.ini')

    if config['DEFAULT']['log_level'] == "DEBUG":
        loglevel = logging.DEBUG
    elif config['DEFAULT']['log_level'] == "INFO":
        loglevel = logging.INFO
    elif config['DEFAULT']['log_level'] == "WARNING":
        loglevel = logging.WARNING
    elif config['DEFAULT']['log_level'] == "ERROR":
        loglevel = logging.ERROR
    elif config['DEFAULT']['log_level'] == "CRITICAL":
        loglevel = logging.CRITICAL
    else:
        loglevel = logging.INFO

    logging.basicConfig(format='%(asctime)s [%(levelname)8s] - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=loglevel)

    logging.debug(vars(args))
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
        if not args.same_dir:
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
                logging.debug(str.format("Checking {}", file))
                fullpath = os.path.join(dir, file)
                results = detector.predict(fullpath, image_size=(224, 224))
                if results[fullpath]['neutral'] <= float(config['DEFAULT']['neutral_percentage']) and \
                        (results[fullpath]['sexy'] >= float(config['DEFAULT']['sexy_percentage']) or
                         results[fullpath]['porn'] >= float(config['DEFAULT']['porn_percentage']) or
                         results[fullpath]['hentai'] >= float(config['DEFAULT']['hentai_percentage'])):
                    logging.debug(file + " is nsfw.")
                    if not args.delete_nsfw:
                        if not args.same_dir:
                            shutil.move(os.path.join(dir, file), os.path.join(dir, str.format("{}/{}", 'nsfw', file)))
                    else:
                        os.remove(fullpath)
                        logging.debug("Deleting " + fullpath)

                    nsfw_count += 1
                else:
                    logging.debug(file + " is sfw.")
                    if not args.delete_sfw:
                        if not args.same_dir:
                            shutil.move(os.path.join(dir, file), os.path.join(dir, str.format("{}/{}", 'sfw', file)))
                    else:
                        os.remove(fullpath)
                        logging.debug("Deleting " + fullpath)
                    sfw_count += 1
            elif args.delete_other and not os.path.isdir(os.path.join(dir, file)):
                os.remove(os.path.join(dir, file))
                logging.info("Deleted " + file)

            processed += 1
            logging.info(
                str.format("[Directory ({}/{}): {}] [Processed: {}/{}] [NSFW: {}] [SFW: {}]", str(processed_dir),
                           str(dircount), str(os.path.basename(dir)), str(processed), str(filecount),
                           str(nsfw_count),
                           str(sfw_count)))
        processed_dir += 1

    logging.info("Done!")
    time.sleep(3)


if __name__ == '__main__':
    main()
