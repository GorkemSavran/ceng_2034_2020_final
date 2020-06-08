import requests
import os
import uuid
import hashlib
import time
import threading
from multiprocessing import Pool, Process, Queue, Manager

urls = ["http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
"http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]

start = time.time()

def download_file(url, file_names, file_name = None, ):
    r = requests.get(url, allow_redirects=True)
    file = file_name if file_name else str(uuid.uuid4())
    open(file, 'wb').write(r.content)
    file_names.append(file)

def do_child_jobs(urls,file_names):
    """
        In the child process,
        in order to download files
        we seperate process to threads
        for speeding up
    """
    print("Child PID: ",os.getpid())
    threads = []
    for url in urls:
        t = threading.Thread(target=download_file,args=(url,file_names,))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

"""
We must have shared memory between process
So we used manager.list()
This is the same as list but shared resource
"""
manager = Manager()
file_names = manager.list()

"""
We start our process
and we have to wait until its finished
We handle waiting job with doing proc.join()
"""
proc = Process(target=do_child_jobs,args=(urls,file_names,))
proc.start()
proc.join()


file_hash_set = set()

def get_hash(file_name):
    return hashlib.md5(open(file_name,'rb').read()).hexdigest()

def check_duplicate(file_hash):
    if file_hash in file_hash_set:
        print("Duplicate")
    else:
        print("Hash is: " + file_hash)
        file_hash_set.add(file_hash)

p = Pool(8)

file_hashes = p.map(get_hash,file_names)
for file_hash in file_hashes:
    check_duplicate(file_hash)

# for file_name in file_names:
#     file_hash = get_hash(file_name)
#     check_duplicate(file_hash)


print("Elapsed time is: " + str(time.time() - start))