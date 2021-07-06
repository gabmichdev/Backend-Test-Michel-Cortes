import atexit
import gc
import os
import signal
import threading
import time

import psutil

bind = "0.0.0.0:8000"

workers = int(os.getenv("CONCURRENCY", default=2))
worker_class = "sync"

preload_app = True

timeout = 10
graceful_timeout = 30

restart_on_rss = int(os.getenv("RESTART_ON_RSS", default=500))


class MemoryWatch(threading.Thread):
    def __init__(self, server, restart_on_rss):
        super().__init__()
        self.daemon = True
        self.server = server
        self.restart_on_rss = restart_on_rss

    def memory_usage(self, pid):
        return int(psutil.Process(pid).memory_info()[0] / 1024.0 / 1024.0)

    def run(self):
        while True:
            time.sleep(60)
            for (pid, worker) in list(self.server.WORKERS.items()):
                pid_memory_usage = self.memory_usage(pid)
                # self.server.log.info("PID %s memory usage: %sMB", pid, pid_memory_usage)
                if pid_memory_usage >= self.restart_on_rss:
                    self.server.log.info(
                        "restart_on_rss on PID %s, observed memory usage: %sMB",
                        pid,
                        pid_memory_usage,
                    )
                    self.server.kill_worker(pid, signal.SIGTERM)


# disable Python GC in master as early as possible
gc.disable()


def when_ready(server):
    # mark preloaded app objects as uncollectable
    gc.freeze()
    # enable child memory watcher
    mw = MemoryWatch(server, restart_on_rss)
    mw.start()


def post_fork(server, worker):
    # reenable GC on worker
    gc.enable()
    # no final GC needed
    atexit.register(os._exit, 0)
