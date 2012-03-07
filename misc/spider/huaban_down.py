from urllib2 import urlopen
with open('huban.link') as huban:
    for line in huban:
        line = line.strip()
        h = urlopen(line)
        print h.headers['Content-Type'], line


