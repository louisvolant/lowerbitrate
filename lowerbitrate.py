#!/usr/local/bin/python3
__author__ = 'Louis Volant'
__version__= 1.0

import logging, json, os, re
from pydub import AudioSegment
from pydub.utils import mediainfo

TARGET_BITRATE = "128k"
# README
# execute with
# $ lowerbitrate % pip install pydub
# $ lowerbitrate % python3 lowerbitrate.py




def get_file_size(file_path):
    file_size = _get_file_size(file_path)
    if file_size is not None:
        return file_size
    return 0

def _get_file_size(file_path):
    try:
        size = os.path.getsize(file_path)
        return size
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def human_readable_number(num):
    suffixes = ['', 'k', 'M', 'B', 'T']
    suffix_index = 0
    num = float(num)

    while num >= 1000 and suffix_index < len(suffixes) - 1:
        num /= 1000.0
        suffix_index += 1

    if suffix_index == 0:
        return str(int(num))
    else:
        return f"{num:.1f}{suffixes[suffix_index]}"

def handleMp3File(inputFilePath):
    original_bitrate = mediainfo(inputFilePath)['bit_rate']
    logging.info('Original Bitrate: {0}. Original size : {1}'
                 .format(human_readable_number(original_bitrate), human_readable_number(get_file_size(inputFilePath))))

    sound = AudioSegment.from_file(inputFilePath)
    sound.export(inputFilePath, format="mp3", bitrate=TARGET_BITRATE)

    updated_bitrate = mediainfo(inputFilePath)['bit_rate']
    logging.info('Updated Bitrate: {0}. Updated size : {1}'
                 .format(human_readable_number(updated_bitrate), human_readable_number(get_file_size(inputFilePath))))



def main():
    dir_path = '.'

    for file_path in os.listdir(dir_path):
        logging.info('Processing: {0}'.format(file_path))
        if(file_path.title().endswith('.Mp3')):
            handleMp3File(file_path)




if __name__ == '__main__':
    ## Initialize logging before hitting main, in case we need extra debuggability
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    main()