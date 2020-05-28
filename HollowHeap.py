from collections import defaultdict
"""
Implementation for two-parent hollow heaps
"""

# global variables used

maxRank = 0
A = [None for _ in range(128)] 

"""
Item Structure

items have a specified node that they are stored into
"""
class Item:
    def __init__(self, data):
        self.val = data
        self.node = None

"""
Node Structure

a node is 'full' if it holds an item; 'hollow' otherwise

newly created node is 'full' - item can be moved to a new node or deleted
nodes are 'hollow' until destroyed
"""
class HeapNode:
    def __init__(self):
        self.item = None # would be null if 'hollow'
        self.key = None

        # rank used for ordering
        self.rank = 0

        # three pointers used to connect
        self.child = None

        # simulating the linked list node within
        self.next = None
        self.ep = None # null if 'full' / at most one ; second parent of u if u has two parents

"""
Using the code below

Utilize them to create our heap

The self.root will contain the root node of the heap that is returned by every function that was created
"""
class HollowHeap:
    def __init__(self):
        self.root = None
        self.size = 0
    
    def insert(self, value, key):
        item = Item(value)
        self.root = insert(item, key, self.root)
        self.size += 1
        return item

    def getMinimum(self):
        return findMin(self.root)

    def reduceKey(self, item, newKey):
        self.root = decreaseKey(item, newKey, self.root)
    
    def deleteItem(self, item):
        self.root = delete(item, self.root)
        self.size -= 1

    def mergeHeap(self, secondHeap):
        self.root = meld(self.root, secondHeap)
        self.size += secondHeap.size

    def deleteMinimum(self):
        self.root = deleteMin(self.root)
        self.size -= 1

"""
Tree Structure

A tree is heap-ordered iif for every tree arc (v,w) : v.key <= w.key (whether or not v and w are hollow), assuming v is the parent of w and w is the child of v.

Heap-order = Tree contains a minimum key (similar to a regular heap)

Therefore - minimum node in a tree = root

Let us assume the maximum amount of values inside this is 10000

maximum rank is log2(10000) = 13
"""


"""
returns a new, empty heap
"""
def makeHeap():

    return None

"""
creates a new node with the item 'e' and key 'k'
"""
def makeNode(e, k):
    u = HeapNode()
    u.item = e
    u.key = k

    e.node = u
    return u

"""
add 'v' into 'w' because v had a larger key - hence lower priority

before:
'w' -> 'w.child'

after:
'w' -> 'v' -> 'w.child'
"""
def addChild(v, w):
    v.next = w.child
    w.child = v
    return

"""
linking two nodes determines the smallest key - breaking equals and links them together as such - returns the PARENT
"""
def link(v, w):
    if v.key >= w.key:
        addChild(v, w)
        return w # returns the parent between the two nodes
    else:
        addChild(w, v)
        return v

"""
return an item of minimum key in heap 'h', null if 'h' is empty
"""
def findMin(h):
    if not h:
        return None
    return h.item # h is the root node of the heap

"""
returns a heap formed by inserting item 'e' with key 'k'. Item e must not exist in any heap
"""
def insert(e, k, h):
    return meld(makeNode(e, k), h)

"""
return a heap formed from non-empty heap 'h' by deleting the item returned by findMin(h)
"""
def deleteMin(h):
    return delete(h.item, h)

"""
return a heap containing all items in item-disjoint heaps h1 and h2

if h1 = None return h2
if h2 = None return h1

otherwise - unite their sets of trees and update the minimum node
"""
def meld(h1, h2):
    if not h1:
        return h2
    if not h2:
        return h1
    return link(h1, h2)

"""
given 'e' is an item in heap h with key greater than k, returns the heap formed from 'h' by changing the key from 'e' to 'k'

If v is a parent of u, we say that v is the first or second parent of u if u acquired parent v via a
link or a decrease-key, respectively. Only a hollow node can have two parents; it can lose them in
either order.

A node u of rank r has exactly r virtual children, of ranks 0, 1, . . . , r − 1, unless r > 2
and u was made hollow by a decrease-key, in which case u has exactly two virtual
children, of ranks r − 2 and r − 1.

"""
def decreaseKey(e, k, h):
    # grab the node that contains the item
    u = e.node
    # check if we found the node associated inside of the heap - checked if its the root
    if u == h:
        u.key = k # update the key of the node with the new key inputted
        return h # returns the heap with the updated data
    
    # decrease on an item not in the minimum node ^ maks the newly hollow node u a child of the new full node 'v'
    v = makeNode(e, k)

    # hollow node - once hollow it can't acquie a new parent AND it can NOT be FULL AGAIN
    u.item = None
    if u.rank > 2: v.rank = u.rank - 2

    # the new node is the parent of the hollow node 'u'
    # set new full node 'v' 
    v.child = u
    u.ep = v # one of the ways to get a parent - the other way is losing a link

    # we do not change u.next: u.next is the next sibling of u on the list of children of the FIRST parent of u
    return link(v, h)

"""
return a heap formed deleting e, assumed to be in h, from h

keep track of roots as they are destroyed and linked.

use list L of hollow roots - singly linked by next pointers
"""
def delete(e, h):
    global maxRank
    global A
    # hollow out the node associated
    e.node.item = None
    e.node = None

    # non minimum deletion - don't have to do anything more
    if h.item: return h
    # while L not empty - all the potential nodes to check
    maxRank = 0
    
    # sever the ties with next node
    h.next = None
    while h:
        w = h.child
        v = h
        h = h.next
        while w:
            u = w
            w = w.next

            # u = w and w is the next node ( u -> w)
            if not u.item:
                # there is no extra parent - move up to the top and set 'u' to be the child
                if not u.ep:
                    # case (a)
                    u.next = h
                    h = u
                # there is an extra parent - assign to ep instead
                else:
                    # case (b)
                    if u.ep == v: w = None
                    # case (c)
                    else: u.next = None

                    # clean up the ep
                    u.ep = None
            # rank the lists - node is FULL
            # case(d)
            else:
                while A[u.rank]:
                    # print("Current rank:", u.rank, u, A[u.rank].rank, A[u.rank], "u:", u.item.val, u.key, "A[u.rank]:",A[u.rank].item.val, A[u.rank].key)
                    u = link(u, A[u.rank])
                    A[u.rank] = None
                    u.rank += 1
                A[u.rank] = u
                if u.rank > maxRank:
                    maxRank = u.rank
        del v
    # empty A and link full roots via unranked until there is at most one
    for i in range(0, maxRank + 1):
        if A[i]:
            if h:
                h = link(h, A[i])
            else:
                h = A[i]                
            A[i] = None
    return h
