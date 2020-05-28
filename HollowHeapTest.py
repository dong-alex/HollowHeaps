import unittest
import heapq
import numpy as np
import time
from collections import defaultdict
from HollowHeap import HollowHeap, Item
from Heap import BinHeap
values = [14,11,5,9,0,8,10,3,6,12,13,4]

class HollowHeapTest(unittest.TestCase):
    def initializeHeap(self):
        heap = HollowHeap()
        references = defaultdict(Item)
        for i in values:
            references[i] = heap.insert(i, i)
        return heap, references

    """
    Tests for the sorted values
    """
    def testGetMinimum(self):
        heap, _ = self.initializeHeap()
        sortedValues = sorted(values)
        for i in sortedValues:
            self.assertEqual(heap.getMinimum().val, i)
            heap.deleteMinimum()
    
    """
    Tests for the decreaseKey
    """
    def testDecreaseKey(self):
        heap, references = self.initializeHeap()
        heap.deleteMinimum()
        # decrease key of 5 to 1
        heap.reduceKey(references[5], 1)
        self.assertEqual(heap.getMinimum().val, 5, "Error in decreasing the key") # should be the item with the key 1 which should have value 5

    """
    Benchmark Testing

    Testing differences between regular heap from heapq module and the hollow heap implementation

    Utilize different sizes for benchmark
    """
    def testBenchmark(self):
        print("Note: Heapq module implementation in C - hence the faster runtimes. Consider the regular binary heap implementation as a more closer representation")
        for size in [500,1000,2000,10000,20000,50000, 100000]:
            regularHeap = []
            hollowHeap = HollowHeap()
            heap = BinHeap()

            # generate random values
            data = [i for i in range(1, size + 1)]
            np.random.shuffle(data)
            
            # time regular binary heap (python)
            binHeapStart = time.time()
            heap.buildHeap(data)
            binHeapEnd = time.time()

            # time regular heapq
            regularHeapStart = time.time()
            for x in data:
                heapq.heappush(regularHeap, x)
            regularHeapEnd = time.time()

            # time hollow heap
            hollowHeapStart = time.time()
            for x in data:
                hollowHeap.insert(x, x)
            hollowHeapEnd = time.time()
            
            print("------------------------------------------")
            print("Time for dataset of", str(size), "values:")
            print("Binary heap implementation:", binHeapEnd - binHeapStart)
            print("Heapq implementation:", regularHeapEnd - regularHeapStart)
            print("Hollow heap implementation:", hollowHeapEnd - hollowHeapStart)

if __name__ == '__main__':
    unittest.main()