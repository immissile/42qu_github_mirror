"""
Pythius - Source code statistics

Copyright (c) 2001 by Jürgen Hermann <jh@web.de>
All rights reserved, see LICENSE for details.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""
# $Id: pystat.py,v 1.2 2001/11/05 22:59:57 jhermann Exp $
__version__ = "$Revision: 1.2 $"[11:-2]

# Globals
spacer = '  '


#############################################################################
### Analyze source file
#############################################################################

class SourceStat:
    def __init__(self):
        self.identifiers = [] # list of identifiers in order of appearance
        self.active = [('TOTAL ', -1, 0)] # stack of active identifiers and indent levels
        self.counters = {} # counters per identifier
        self.indent_level = 0

    def indent(self, tok):
        self.indent_level += 1

    def dedent(self, tok):
        self.indent_level -= 1
        if self.indent_level < 0:
            raise ValueError("INTERNAL ERROR: Negative indent level")

        # remove identifiers of a higher indentation
        while self.active and self.active[-1][1] >= self.indent_level:
            counters = self.counters.setdefault(self.active[-1][0], {})
            counters['start'] = self.active[-1][2]
            counters['end'] = tok.row - 1
            counters['lines'] = tok.row - self.active[-1][2]
            del self.active[-1]

    def push(self, identifier, row):
        if len(self.active) > 1:
            qualified = self.active[-1][0] + '.' + identifier
        else:
            qualified = identifier
        self.active.append((qualified, self.indent_level, row))
        self.identifiers.append(qualified)

    def inc(self, key, value=1):
        for id, level, row in self.active:
            counters = self.counters.setdefault(id, {})
            counters[key] = counters.setdefault(key, 0) + value

    def dump(self):
        label_len = 79 - len(spacer) - 6 * 6
        util.log(spacer + "FUNCTION / CLASS".ljust(label_len) +
            " START   END LINES  NLOC  COMM EMPTY")
        for id in self.identifiers + ['TOTAL ']:
            if id.count('.') >= list_depth: continue

            label = spacer * id.count('.') + id.split('.')[-1]
            counters = self.counters.get(id, {})
            msg = spacer + label.ljust(label_len)

            for key in ('start', 'end', 'lines', 'nloc', 'comments', 'empty'):
                if counters.get(key, 0):
                    msg += " %5d" % (counters[key], )
                else:
                    msg += " " * 6

            util.log(msg)

    def getCounter(self, id, key):
        return self.counters.get(id, {}).get(key, 0)


def summarize(total, key, value):
    total[key] = total.setdefault(key, 0) + value
    return value


def analyze(filename, total):
    """ Analyze a source file.
    """
    from pythius import grok

    file = open(filename, 'r')
    try:
        source = file.read()
    finally:
        file.close()

    parser = grok.Parser()
    parser.parse(source)

    util.log("\n%s (%d lines, %d bytes)" % (
        filename,
        summarize(total, 'lines', parser.lines),
        summarize(total, 'bytes', len(source)),
        ))

    stats = SourceStat()
    stats.inc('lines', parser.lines)
    comments = 0
    empty = 0
    for idx in range(len(parser.tokenlist)):
        tok = parser.tokenlist[idx]

        # counting
        if tok.type == grok.NEWLINE:
            stats.inc('nloc')
        if tok.type == grok.COMMENT:
            stats.inc('comments')
        if tok.type == grok.EMPTY:
            stats.inc('empty')

        if tok.type == grok.INDENT: stats.indent(tok)
        if tok.type == grok.DEDENT: stats.dedent(tok)

        if tok.type == grok.KEYWORD:
            if tok.text in ("class", "def"):
                stats.push(parser.tokenlist[idx+2].text, tok.row)

    stats.dump()
    summarize(total, 'comments', stats.getCounter('TOTAL ', 'comments'))
    summarize(total, 'empty lines', stats.getCounter('TOTAL ', 'empty'))
    summarize(total, 'non-commentary lines', stats.getCounter('TOTAL ', 'nloc'))


#############################################################################
### Main program
#############################################################################

def usage():
    """ Print usage information.
    """
    import os, sys
    sys.stderr.write("""
%s v%s, Copyright (c) 2001 by Jürgen Hermann <jh@web.de>

Usage: %s [options] [files...]

Options:
    -d, --depth <value>     Report up to given nesting level (default: 1)
    -q, --quiet             Be quiet (no informational messages)
    --full                  Report all available information
    --help                  This help text
    --version               Version information

""" % ('pystat', __version__, 'pystat'))
    sys.exit(1)


def version():
    """ Print version information.
    """
    import os, sys
    from pythius import version
    sys.stderr.write("%s (%s %s [%s])\n" %
        (__version__, version.project, version.release, version.revision))
    sys.exit(1)


def main():
    """ pystat's main code.
    """
    import getopt, sys

    #
    # Check parameters
    #
    try:
        optlist, args = getopt.getopt(sys.argv[1:],
            'd:q',
            ['depth=', 'full', 'help', 'quiet', 'version'])
    except:
        util.fatal("Invalid parameters!", usage=1)

    if util.haveOptions(optlist, ["--version"]): version()
    if not args or util.haveOptions(optlist, ["--help"]): usage()

    util.flag_quiet = util.haveOptions(optlist, ["-q", "--quiet"])

    global flag_full, list_depth

    flag_full = util.haveOptions(optlist, ["--full"])
    if flag_full: list_depth = 9999
    else: list_depth = 1

    depth = util.getOption(optlist, ["-d", "--depth"])
    if depth: list_depth = int(depth)

    #
    # Collect file names
    #
    files = []
    for name in args:
        files.extend(util.getFilesForName(name))
    util.log("Found %d file%s." % (len(files), ("", "s")[len(files) != 1], ))

    if not files: return

    #
    # Process the files
    #
    total = {}
    summarize(total, 'files', len(files))
    for filename in files:
        analyze(filename, total)

    #
    # Print summary
    #
    util.flag_quiet = 0 # always print summary
    title = 'Summary on "%s"' % (' '.join(args))
    util.log("\n%s\n%s" % (title, "=" * len(title), ))
    for key in ['files', 'lines', 'bytes', 'comments',
                'empty lines', 'non-commentary lines']:
        util.log(key.ljust(20) + "%6d" % total[key])
    util.log("")


def run():
    global util
    from pythius import util
    util.runMain(main)


if __name__ == "__main__": run()

