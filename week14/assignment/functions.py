"""
Course: CSE 251, week 14
File: common.py
Author: Roberto Reynoso

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family = Request_thread(f'{TOP_API_URL}/family/{id}')

Requesting an individual from the server:
person = Request_thread(f'{TOP_API_URL}/person/{id}')


You will lose 10% if you don't detail your part 1 
and part 2 code below

Describe how to speed up part 1

Depth-First can first check the root then will either check the left side of the root,
then the right side of the tree. If you were going root, left, and right that is called
Pre-order. Left, root, and right is called Inorder.Left, right and root is called Postorder.

You could potentially check call in Depth-First in its own thread, it could be faster.

Describe how to speed up part 2

Breadth-First goes by level order within the tree. So the root is level 0 and then it goes down
from there to level 1 and so on.

With this assignment being on family tree's that can be split into levels from spouses to children,
then you could use threads to complete each level at once, to speed it up.


10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *

# -----------------------------------------------------------------------------


def depth_fs_pedigree(family_id, tree):
    # TODO - implement Depth first retrieval

    if family_id == None or tree.does_family_exist(family_id):
        return

    print(f"Getting Family: {family_id}")
    req = Request_thread(f'{TOP_API_URL}/family/{id}')
    req.start()
    req.join()
    family = Family(family_id, req.response)
    tree.add(family)


# -----------------------------------------------------------------------------


def breadth_fs_pedigree(start_id, tree):
    # TODO - implement breadth first retrieval

    print('WARNING: BFS function not written')

    pass


# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_id, tree):
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5

    print('WARNING: BFS (Limit of 5 threads) function not written')

    pass
