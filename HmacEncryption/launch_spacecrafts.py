import sys
from spacecraft_inst import spacecraft_inst
from threading import Thread, Lock

pop = int(sys.argv[1])

def launch(id,lock):
    print(f'The spacehip {id} has been launched')
    s = spacecraft_inst(id,lock)
    s.launch()
    
lock = Lock()

# create and start 10 threads
threads = []
for n in range(1, pop+1):
    t = Thread(target=launch, args=(n,lock))
    threads.append(t)
    t.start()

# wait for the threads to complete
for t in threads:
    t.join()
