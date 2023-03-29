import logging
import sys

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    for line in sys.stdin:
        if 'exit' == line.rstrip():
            break
        print(f'Processing Message from sys.stdin *****{line}*****')
    print("Done")
