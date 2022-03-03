from platform_collector import Platform
from utilites import time_track


@time_track
def start_collecting():
    oz = Platform('oz')
    # wb = Platform('wb')
    oz.start()
    # wb.start()
    oz.join()
    # wb.join()


if __name__ == '__main__':
    start_collecting()
