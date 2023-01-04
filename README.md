# Key Slot Utility  

## Contents
1.  [Summary](#summary)
2.  [Features](#features)
3.  [Prerequisites](#prerequisites)
4.  [Installation](#installation)
5.  [Usage](#usage)

## Summary <a name="summary"></a>
This is a utility script for determining the key slot and node location for a given key string.

## Features <a name="features"></a>
- Calculate key slot based on the Redis hash slot algorithm
- Interrogates a Redis Enterprise cluster via REST API to determine the node assignment for a hash slot
- Can be compiled to a single binary via Nuitka 

## Prerequisites <a name="prerequisites"></a>
- Python

## Installation <a name="installation"></a>
1. Clone this repo.

2.  Install Python requirements
```bash
pip install -r requirements.txt
```

3.  Optional.  Compile Python app to an executable (binary)
```bash
./compile.sh
```

## Usage <a name="usage"></a>
### Options
- --url. Redis REST API base URL
- --user.  Redis REST API user name
- --password. Redis REST API user password
- --dbid.  Database ID (int) of the db to be queried for node/slot assignments  

### Examples for the given RE cluster
![rladmin](screenshot.png "rladmin")  

### Key = foo
#### Python
```bash
python3 keyslot.py --url https://localhost:19443 --user redis@redis.com --password redis --dbid 1 foo
```
#### Binary
```bash
./ks --url https://localhost:19443 --user redis@redis.com --password redis --dbid 1 foo
```
#### Result
```bash
{'key': 'foo', 'slot': 12182, 'node': 2}
```  

### Key = foo{bar}
#### Python
```bash
python3 keyslot.py --url https://localhost:19443 --user redis@redis.com --password redis --dbid 2 foo{bar}
```
#### Binary
```bash
./ks --url https://localhost:19443 --user redis@redis.com --password redis --dbid 2 foo{bar}
```
#### Result
```bash
{'key': 'bar', 'slot': 5061, 'node': 1}
```

### Key = foo{}{bar}
#### Python
```bash
python3 keyslot.py --url https://localhost:19443 --user redis@redis.com --password redis --dbid 2 foo{}{bar}
```
#### Binary
```bash
./ks --url https://localhost:19443 --user redis@redis.com --password redis --dbid 2 foo{}{bar}
```
#### Result
```bash
{'key': 'foo{}{bar}', 'slot': 8363, 'node': 3}
```


