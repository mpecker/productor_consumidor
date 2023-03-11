#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:50:36 2023

@author: mariapeckergayarre
"""

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
from random import random, randint


N = 50
NPROD = 3

def delay(factor = 3):
    sleep(random()/factor)

def producer(storage, empty, non_empty, i):
    current=0
    for v in range(N):
        current += randint(0,5)
        print (f"producer {current_process().name} produciendo")
        delay(6)
        empty.acquire()
        storage[i]= current
        non_empty.release()
        print (f"producer {current_process().name} almacenado {v}")
    empty.acquire()
    storage[i]=-1
    non_empty.release()


def consumer(storage, empty, non_empty):
    for n in range(NPROD):
        non_empty[n].acquire()
    print (f"consumer {current_process().name} desalmacenando")
    lista=[]
    ind=1
    while max(storage)>-1:
        minimo=max(storage)+1
        for i in range(NPROD):
            if storage[i]>-1 and storage[i]<minimo:
                minimo=storage[i]
                ind=i
        lista.append(minimo)
        empty[ind].release()
        print (f"consumer {current_process().name} consumiendo {minimo}")
        non_empty[ind].acquire()
    print(lista)
    delay()

def main():
    storage = Array('i', NPROD)
    index = Value('i', 0)
    for i in range(NPROD):
        storage[i] = -2
    print ("almacen inicial", storage[:], "indice", index.value)

    non_empty = [ Semaphore(0) for _ in range(NPROD)]
    empty = [ BoundedSemaphore(1)  for _ in range(NPROD)]

    prodlst = [ Process(target=producer,
                        name=f'prod_{i}',
                        args=(storage, empty[i], non_empty[i], i))
                for i in range(NPROD) ]

    conslst = [ Process(target=consumer,
                      args=(storage, empty, non_empty))]

    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()


if __name__ == '__main__':
    main()
