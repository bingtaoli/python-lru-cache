#!/usr/bin/env python
# coding: utf8
import time


class Node:

    def __init__(self):
        self.expire = 0
        self.key = None
        self.prev = None
        self.next_node = None


def queue_init(size):
    q = []
    for i in range(size+1):
        q.append(Node())
    if size == 0:
        q[0].prev = q[0]
        q[0].next_node = q[0]
    else:
        prev = q[0]
        for i in range(1, size+1):
            e = q[i]
            prev.next_node = e
            e.prev = prev
            prev = e
        last_node = q[size]
        last_node.next_node = q[0]
        q[0].prev = last_node
    return q


def queue_is_empty(q):
    return q[0].prev == q[0]


def queue_remove(x):
    prev_node = x.prev
    next_node = x.next_node
    prev_node.next_node = next_node
    next_node.prev = prev_node


def queue_insert_head(q, x):
    x.next_node = q[0].next_node
    x.next_node.prev = x
    x.prev = q[0]
    q[0].next_node = x


def queue_last(q):
    return q[0].prev


def queue_head(q):
    return q[0].next_node


class LRUCache:

    def __init__(self, size):
        self.key_to_node = {}
        self.hash_table = {}
        self.cache_queue = queue_init(0)
        self.free_queue = queue_init(size)

    def get(self, key):
        cache_queue = self.cache_queue
        hash_table = self.hash_table
        key_to_node = self.key_to_node
        value = hash_table.get(key)
        if value is None:
            return None
        node = key_to_node[key]
        queue_remove(node)
        queue_insert_head(cache_queue, node)
        if 0 < node.expire < time.time():
            return None
        return value

    def delete(self, key):
        hash_table = self.hash_table
        free_queue = self.free_queue
        key_to_node = self.key_to_node
        hash_table[key] = None
        node = key_to_node.get(key)
        if node is None:
            return
        node.key = None
        queue_remove(node)
        queue_insert_head(free_queue, node)

    def set(self, key, value, ttl=None):
        cache_queue = self.cache_queue
        free_queue = self.free_queue
        hash_table = self.hash_table
        key_to_node = self.key_to_node
        hash_table[key] = value
        node = key_to_node.get(key)
        if not node:
            if queue_is_empty(free_queue):
                # print "free_queue is empty"
                node = queue_last(cache_queue)
                old_key = node.key
                del hash_table[old_key]
                del key_to_node[old_key]
            else:
                # print "use head of free_queue"
                node = queue_head(free_queue)
            node.key = key
            key_to_node[key] = node
        queue_remove(node)
        queue_insert_head(cache_queue, node)
        if ttl:
            node.expire = time.time() + ttl
        else:
            node.expire = -1


if __name__ == '__main__':
    lru_cache = LRUCache(10)
    lru_cache.set('a', 10)
    print lru_cache.get('a')
    lru_cache.set('b', 20)
    print lru_cache.get('b')
    for i in range(30):
        lru_cache.set(i, 'hello, world')
    print lru_cache.get(20)
    print lru_cache.get(21)
    print lru_cache.get('a')
    lru_cache.set('a', 10)
    print lru_cache.get('a')
    lru_cache.set('b', 20, 1)
    time.sleep(2)
    print lru_cache.get('b')

