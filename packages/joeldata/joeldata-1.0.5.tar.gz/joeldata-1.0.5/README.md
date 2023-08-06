# JoelData
Simple data types I use in my projects.
```py
pip3 install joeldata
```


# Documentation
## Stack
FIFO (like a stack of cups)

```py
from joeldata import Stack
my_stack=Stack()
```

* `push(item)` - adds new item
* `pop() -> item` - removes item
* `peek() -> item` - see top item without removing
* `is_empty() -> bool`


## Queue
LIFO (like a line at a store)

```py
from joeldata import Queue
my_q=Queue()
```

* `enqueue(item)` - add new item
* `dequeue() -> item` - remove an item
* `peek() -> item` - see the item that next to be dequeued
* `is_empty() -> bool`



## BST (aliased to Binary Search Tree)
Stores a list of numbers in a tree where each node can have up to two chiuldren. The left node is always less than the parent node and the right node is always greater than the parent node.

```py
from joeldata import BST
my_bst=BST()
```

* `add(item)` - adds an item to the BST
* `search(value) -> bool` - sees if a value is in the BST
* `inorder() -> item[]` - returns the items as an array in order
* `remove(item)` - removes an item from the BST


# HashTable
Implementation of the object in JavaScript, `java.util.HashMap` in Java, and dictionary in Python.

```py
from joeldata import HashTable
my_ht=HashTable()
```

* `get(key) -> value` - returns the HashMap's value of the key
* `set(key, value)` - sets the HashMap to your value at the key
* `clear()` - removes all the key-value pairs, emptying the HashMap.
* `remove(key) -> value` - removes the key-value pairs at the specified key. Returns the removed value.
* `size() -> int` - returns the number of key-value pairs.
* `is_empty() -> bool` - returns whether or not the HashMap has no key-value pairs.
* `has(key) -> bool` - returns whether or not the HashMap has a key-value pair of the specified key.
* `keys() -> any[]` - returns all the keys of the HashMap in an array.
* `values() -> any[]` - returns all the values of the HashMap in an array.
* `inspect() -> str` - returns the raw self.data for development purposes


## Example
```py
>>> from joeldata import HashTable
>>> ht=HashTable()
>>> ht.set('hi', 'world')
>>> ht.get('hi')
'world'
>>> ht.set('things', ['joel', 'bowl'])
>>> print(ht)
HashTable {
	things: ['joel', 'bowl'],
	hi: world
}
>>> ht.has('hi')
True
>>> ht.size()
2
>>> ht.keys()
['things', 'hi']
>>> ht.values()
[['joel', 'bowl'], 'world']
>>> ht.remove('things')
['joel', 'bowl']
>>> print(ht)
HashTable {
	hi: world
}
>>> ht.clear()
>>> print(ht)
{}
```

