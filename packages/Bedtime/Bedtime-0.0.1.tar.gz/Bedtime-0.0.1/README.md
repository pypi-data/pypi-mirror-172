# bedtime

Python library for doing something when it's almost time for bed (the computer is going to sleep, or turning off).

```py
import time, bedtime

def do_log():
    with open("./test.log", "a") as f:
        f.write("i went to sleep\n")

sleeper = bedtime.Listener(on_sleep=do_log)

while True:
    time.sleep(1)

    # later, after lights out...
    # test.log <
    #   i went to sleep
```

TODO:
* [x] Windows
* [ ] MacOS
* [ ] Linux (maybe usually the same as MacOS?)