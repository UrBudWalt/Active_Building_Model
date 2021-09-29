from threading import Thread
import time
import os

answer = None


def ask():
    global start_time, answer
    start_time = time.time()
    answer = input("Enter a number:\n")
    time.sleep(0.001)


def timing():
    time_limit = 5
    while True:
        time_taken = time.time() - start_time
        if answer is not None:
            print(f"You took {time_taken} seconds to enter a number.")
            os._exit(1)
        if time_taken > time_limit:
            print("Time's up !!! \n"
                  f"You took {time_taken} seconds.")
            os._exit(1)
        time.sleep(0.001)


t1 = Thread(target=ask)
t2 = Thread(target=timing)
t1.start()
t2.start()