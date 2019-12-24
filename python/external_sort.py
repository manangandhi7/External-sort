#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import shutil
import os

# buffer size is the max number your memory can handle, set a small number in the beginning for trial here
buffer_size = 10000
# total size of the number that needs to be sorted, only needed if you want to generate a file of unsorted integers
total_size = 55000

def save_array_to_file(file_name, array_to_save):
    np.savetxt(file_name, array_to_save, fmt = '%d')
    
def sort_and_write(file_name, array_to_sort):
    array_to_sort.sort()
    save_array_to_file(file_name, array_to_sort)
    
def read_n_int(file_, numbers_to_read):
    array_ = []
    
    if numbers_to_read <= 0 :
        return array_
    
    num = file_.readline()
    while(num):
        array_.append(int(num))
        if len(array_) >= numbers_to_read:
            break
        num = file_.readline()
            
    return array_

def create_unsorted_file(size_, file_name_ = 'unsorted.csv'):
    arr = np.arange(size_)
    np.random.shuffle(arr)
    save_array_to_file(file_name_, arr)
    arr = None
    
import heapq

def sort_slices(file_name, buffer_size_):
    read_arr = []
    chunk = 1
    f = open(file_name)

    if os.path.exists('./tmp/'):
        shutil.rmtree('./tmp/')
    os.mkdir('./tmp/')

    #TODO : delete contents of tmp directory
    read_arr = read_n_int(f, buffer_size_)
    while (len(read_arr) > 0):
        sort_and_write('./tmp/sorted_' + str(chunk), read_arr)
        read_arr = read_n_int(f, buffer_size_)
        chunk = chunk + 1

    f.close()

def min_heap_sort(output_file):
    sorted_file = open(output_file, 'w+')

    min_heap = []
    heapq.heapify(min_heap)
    
    open_files = []
    for f in os.listdir('./tmp/'):
        if os.path.isfile('./tmp/' + f):
            file_ = open('./tmp/' + f)
            open_files.append(file_)
            val = file_.readline()
            heapq.heappush(min_heap, (int(val), file_))

    while(len(min_heap) > 0):
        min_element = heapq.heappop(min_heap)
        sorted_file.write(str(min_element[0]) + '\n')
        next_str = min_element[1].readline()
        if next_str:
            heapq.heappush(min_heap, (int(next_str), min_element[1]))
        else:
            min_element[1].close()

    sorted_file.close()

def external_sort(input_file, output_file, buffer_size_ = 10000):
    sort_slices(input_file, buffer_size_)
    min_heap_sort(output_file)
    print('Sorted values are written to' , str(output_file))
    
create_unsorted_file(total_size, file_name_ = 'unsorted.csv')

external_sort(input_file= 'unsorted.csv', output_file='sorted_external.csv', buffer_size_ = buffer_size)


# In[ ]:




