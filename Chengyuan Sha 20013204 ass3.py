# Written by Chengyuan Sha 2013204
# This assignment implements AVL tree and MaxHeap to mimic web search engine

from os import listdir
from os.path import isfile, join

# node for AVL tree
class TreeNode: 
    def __init__(self, key, value): 
        self.key = key
        self.value = value 
        self.left = None
        self.right = None
        self.height = 1

# AVL tree class
class AVLTreeMap:
    def __init__(self):
        self.root = None

    # this function returns the height of current AVL tree
    def getHeight(self, cur): 
        if cur is None: 
            return 0
        return cur.height 

    # calculate balance factor 
    def getBalanceFactor(self, cur):
        if cur is None:
            return 0
        return self.getHeight(cur.left) - self.getHeight(cur.right) 

    # try to balance: left rotation 
    def leftRotate(self, gp): 
        son = gp.right 
        sonLeft = son.left 
        # Perform rotation 
        son.left = gp 
        gp.right = sonLeft 
        # Update heights 
        gp.height = 1 + max(self.getHeight(gp.left), self.getHeight(gp.right)) 
        son.height = 1 + max(self.getHeight(son.left), self.getHeight(son.right)) 
        # Return the new root 
        return son 

     # try to balance: right rotation 
    def rightRotate(self, gp): 
        son = gp.left 
        sonRight = son.right 
        # Perform rotation 
        son.right = gp 
        gp.left = sonRight 
        # Update heights 
        gp.height = 1 + max(self.getHeight(gp.left), self.getHeight(gp.right)) 
        son.height = 1 + max(self.getHeight(son.left), self.getHeight(son.right)) 
        # Return the new root 
        return son 

    # following the outline in the course note
    # This function adds ndoes to a tree and adjust the structure to maintain a valid AVL tree
    def putHelper(self, cur, key, value):
        # Step 1 - Perform normal BST 
        if not cur: 
            return TreeNode(key, value) 
        if key < cur.key:
            cur.left = self.putHelper(cur.left, key, value)
        elif key > cur.key:
            cur.right = self.putHelper(cur.right, key, value)
        else: # key == cur.key, update the value
            cur.value = value
        # Step 2 Update the height of ancestor node 
        cur.height = 1 + max(self.getHeight(cur.left), self.getHeight(cur.right)) 
        # Step 3 - Get the balance factor 
        balance = self.getBalanceFactor(cur) 
        # Step 4 - If the node is unbalanced, try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and key < cur.left.key: 
            return self.rightRotate(cur) 
        # Case 2 - Right Right 
        if balance < -1 and key > cur.right.key: 
            return self.leftRotate(cur) 
        # Case 3 - Left Right 
        if balance > 1 and key > cur.left.key: 
            cur.left = self.leftRotate(cur.left) 
            return self.rightRotate(cur) 
        # Case 4 - Right Left 
        if balance < -1 and key < cur.right.key: 
            cur.right = self.rightRotate(cur.right) 
            return self.leftRotate(cur) 
        return cur

    # insert a new key-value pair
    def put(self, key, value):
        self.root = self.putHelper(self.root, key, value)
        return

    # ~~~~~print tree, used for debug purpose~~~~~~~~
    def printHelper(self, root, indent):
        if root is not None:
            self.printHelper(root.right, indent+"  ")
            print(indent + str(root.key))
            self.printHelper(root.left, indent+"  ")

    def printTree(self):
        return self.printHelper(self.root, indent="")

    # ~~~~~print tree value, used for debug purpose~~~~~
    def printHelperVal(self, root, indent):
        if root is not None:
            self.printHelperVal(root.right, indent+"  ")
            print(indent + str(root.value))
            self.printHelperVal(root.left, indent+"  ")

    def printTreeVal(self):
        return self.printHelperVal(self.root, indent="")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

    # This function returns the value if the given key exists in the AVL tree
    # This function returns None if not found
    def getHelper(self, cur, key):
        # key not found
        if cur is None:
            return None
        if key == cur.key:
            return cur.value
        elif key < cur.key:
            return self.getHelper(cur.left, key)
        else:
            return self.getHelper(cur.right, key)

    # pass root to getHelper
    def get(self, key):
        return self.getHelper(self.root, key)

    # This function returns a list of all the keyss visited on the search path
    def searchHelper(self, cur, key, searchList=[]):
        if cur is None: # when value is not found
            searchList.append("key not in the tree")
            return searchList 
        searchList.append(cur.key)
        if key == cur.key:
            return searchList
        elif key < cur.key:
            return self.searchHelper(cur.left, key, searchList)
        else: # cur.key > key
            return self.searchHelper(cur.right, key, searchList)

    # pass root to searchHelper
    def searchPath(self, key):
        return self.searchHelper(self.root, key)

# This class contains the index representation of a web page. It transfers a web page (textfile in this assignment) into an AVLTreeMap
# Each key refers to each word appearing in the document, and each value represents a list containing the positions of this word in the file.
class WebPageIndex:
    # a constructor taking a file name as input.
    def __init__(self, filename):
        self.name = filename
        avltree = AVLTreeMap()
        wordList = self.readFile(filename)
        for i in wordList:
            avltree.put(i, self.indexPosition(wordList, i))
        self.AVLIndex = avltree 

    # read a txt file provided for this assignment
    def readFile(self, filename):
        with open(filename, 'r') as f:
            wordList = []
            for lines in f:
                for word in lines.split():
                    # strip all non-alpha character in word and convert to lower case
                    onlyAlpha = (''.join([char for char in word if char.isalpha()])).lower()
                    wordList.append(onlyAlpha)
        return wordList

    # return a list containing the all positions in the file
    def indexPosition(self, lst, item):
        return [i for i, x in enumerate(lst) if x == item]

    # this function returns the number of times a word appeared on the page
    def getCount(self, s):
        rslt = self.AVLIndex.get(s)
        if rslt is None:
            return 0
        else:
            return len(rslt)

# array implementation of MaxHeap 
class MaxHeap:
    def __init__(self):
        self.heap = []

    # makes easier to find left child's index
    def leftChildLoc(self, index):
        return 2*index + 1

    # makes easier to find right child's index
    def rightChildLoc(self, index):
        return 2*index + 2

    # makes easier to find parent's index
    def parentLoc(self, index):
        return (index-1)//2

    # change the value of 2 positions
    def swap(self, a, b):
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]
        return

    # insert a node based on it's priority value
    def insert(self, node):
        self.heap.append(node)
        valIndex = len(self.heap) - 1
        while ((self.heap[valIndex].pri) > (self.heap[self.parentLoc(valIndex)]).pri) and (valIndex > 0):
            self.swap(valIndex, self.parentLoc(valIndex))
            valIndex = self.parentLoc(valIndex)
        return

    # see the max value in the heap without removing it
    def peekMax(self):
        if self.heap == []:
            return None
        else:
            return self.heap[0]

    # delete the max value in the heap and rebalance the heap
    def delMax(self):
        N = len(self.heap) 
        if N == 0:
            return None
        maxVal = self.heap[0]
        if N == 1:
            del self.heap[0]
            return maxVal
        #print(self.heap[0])
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        del self.heap[-1]
        k = 0
        while (self.leftChildLoc(k) <= len(self.heap)-1) :
            j = self.leftChildLoc(k)
            if (j < (len(self.heap)-1)) and (self.heap[j].pri < self.heap[j+1].pri):
                j += 1
            if not (self.heap[k].pri < self.heap[j].pri):
                break;
            self.swap(k, j)
            k = j
        return maxVal

# heap node stores priority and webPageIndex instance inside
class HeapNode:
    def __init__(self, priority, webPageIndex):
        self.pri = priority
        self.webPageIndex = webPageIndex

# it uses maxheap to hold the data items in the priority queue
class WebpagePriorityQueue:
    def __init__(self, query, webpageIndex):
        self.webIndexList = webpageIndex
        self.query = query
        self.maxHeap = self.createHeap(query) 

    # creat a max heap based on priority
    def createHeap(self, query):
        maxHeap = MaxHeap()
        queryList = query.split() # query may be more than 1 word
        for i in self.webIndexList:
            heapNode = HeapNode(self.calPriority(queryList, i), i)
            maxHeap.insert(heapNode)
        return maxHeap
        
    # calculate the priority of a query in a web
    def calPriority(self, queryList, webpageIndex):
        priority = 0
        for i in queryList:
            priority += webpageIndex.getCount(i)
        return priority

    # Return the highest priority (largest value) item in the WebpagePriorityQueue, without removing it
    def peek(self):
        return self.maxHeap.peekMax()

    # Remove and return the highest priority item in the WebpagePriorityQueue
    def poll(self):
        return self.maxHeap.delMax()

    # takes a new query as input and reheap the WebpagePriorityQueue
    def reheap(self, query):
        self.query = query
        self.maxHeap = self.createHeap(query)
        return

# This class implements a simple web search engine
class ProcessQueries:
    # ProcessQueries takes directory name, query file name(in the same path) and user limit in order.
    # user limit default is -1 means we want to show all documents
    def __init__(self, mypath, queryFile, userLimit=-1):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))] # get file names inside a directory
        webInstance = []
        queryList = self.openQueries(queryFile)
        # build a list of WebPageIndex instances from a folder containing a set of web pages (txt files)
        for i in onlyfiles:
            webInstance.append(WebPageIndex(mypath + "/" + i))
        self.display(queryList, webInstance, userLimit)

    # enter a loop to process a series of user queries
    def display(self, queryList, webInstance, userLimit):
        count = 0
        while (count < len(queryList)):
            limit = 0
            pq = WebpagePriorityQueue(queryList[count], webInstance)
            print("query is: ", end='')
            print(queryList[count])
            while pq.peek() and (limit < userLimit or userLimit == -1):
                deleted = pq.poll()
                print(deleted.webPageIndex.name, end='')
                print("  priority: ", end='')
                print(deleted.pri)
                limit += 1
            count += 1
            if count < len(queryList):
                pq.reheap(queryList[count])
            print("")

    # read the query file and put query into a list
    def openQueries(self, filename):
        with open(filename, 'r') as f:
            queryList = []
            for lines in f:
                queryList.append(lines.strip('\n'))
        return queryList


def main():
    # ProcessQueries takes directory name, query file name(in the same path) and user limit (int) in order.
    pro = ProcessQueries("test data", "queries.txt",5)

if __name__ == '__main__':
    main()


