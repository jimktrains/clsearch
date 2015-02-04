import gzip
import hashlib
import os
import errno


def write(key, val):
    (url_dir, url_file) = filename(key)
    mkdir_p(url_dir)

    with gzip.open(url_file, "wb+") as f:
      f.write(val)

def get(key):
    (url_dir, url_file) = filename(key)

    if os.path.exists(url_file):
        with gzip.open(url_file, "rb") as f:
          return f.read()
    return None

def remove(key):
    (url_dir, url_file) = filename(key)
    os.remove(url_file)

def filename(key):
    url_md5  = hashlib.md5(key).hexdigest()
    url_dir  = "files/" + url_md5[0:2] + "/" + url_md5[2:4]
    url_file = url_dir + "/" + url_md5[4:]

    return (url_dir, url_file)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
