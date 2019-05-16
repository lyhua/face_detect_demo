import threading

def handle(sid):
    while True:
        print("Thread %d run"%sid)

if __name__ == "__main__":
    for i in range(1, 3):
        t = threading.Thread(target=handle, args=(i,))
        t.start()
    while True:
        print("main thread")