import os, sys

def lock(fd):
    import fcntl, errno
    try:
        fcntl.lockf(fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
    except IOError, e:
        if e.errno in (errno.EACCES, errno.EAGAIN):
            print >> sys.stderr, 'There is an instance of', sys.argv[0], 'running. Quit'
            sys.exit(0)
        else:
            raise

def single_process(f):
    lock_file_name = os.path.abspath(sys.argv[0]).lstrip('/').replace('/', '_') + '.lock'
    lock_file_path = os.path.join('/tmp/', lock_file_name)
    def _(*a, **kw):
        fd = os.open(lock_file_path, os.O_CREAT|os.O_RDWR, 0660)
        try:
            lock(fd)
            return f(*a, **kw)
        finally:
            os.close(fd)
    return _
