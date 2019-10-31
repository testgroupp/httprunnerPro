# coding=utf-8
from httprunner.api import HttpRunner
import threading
import time


class MyThread(threading.Thread):
    def __init__(self, suite):
        super(MyThread, self).__init__()
        self.suite = suite

    def run(self):
        runner = HttpRunner(failfast=False)
        runner.run(self.suite)


if __name__ == '__main__':
    suites = ["testsuites/md1.yml", "testsuites/md2.yml"]

    # threads = []
    for suite in suites:
        thread = MyThread(suite)
        thread.start()
        time.sleep(3)
        # threads.append(thread)
