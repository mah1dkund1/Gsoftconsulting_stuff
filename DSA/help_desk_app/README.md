Time complexity of the diferent functions of help desk class



**Raise Ticket** | O(1) | 

Modifying the tail pointer to append to a linked list takes constant time. Dictionary assignments and set insertions are also average O(1). |


| **Resolve Ticket** | O(1) |

 Updating the head pointer to sever the front node from the linked list takes constant time. Appending to Python lists (history and stack) is O(1). |


| **Undo Action** | O(N) |

 Popping from the stack and inserting at the head of the linked list are O(1). However, removing the ticket from the resolved_history array using .remove() requires iterating through the list, making the overall method O(N) where N is the history size. |

| **ID Lookup** | O(1) | Python dictionaries use hash tables, providing instant lookups by key. |