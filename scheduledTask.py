import datetime
import time
from app.controller.util.getAllMovies import getAllMovies
from app.controller.util.getDetails import getDetails

def main(h=0, m=0):
    while True:
        while True:
            now = datetime.datetime.now()
            if now.hour == h and now.minute == m:
                break;
            time.sleep(30)
        try:
            getAllMovies()
            getDetails()
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    main(14,18)

