# python-lru-cache

This repo is inspired by https://github.com/openresty/lua-resty-lrucache

### Synopsis

create an cache with capacity of 10

```py
lru_cache = LRUCache(10)
lru_cache.set('b', 20, 1)
print lru_cache.get('b')
time.sleep(2)  # expire
print lru_cache.get('b')
```

### description

use a double linked list to store usage order. use a simple dict to store key=>value.



