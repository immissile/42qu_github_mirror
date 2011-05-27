"""
    Pythius - Indent/Detab Python Source

    All rights reserved, see LICENSE for details.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    $Id: pydent.py,v 1.2 2001/11/05 22:59:57 jhermann Exp $
"""
__version__ = "$Revision: 1.2 $"[11:-2]

# Globals
_debug = 0

flag_backup = 1
flag_compile = 0
flag_dryrun = 0

#############################################################################
### Indent and detab Python source
#############################################################################

class Indenter:
    """ Fix python source code so that it uses the canonical
        4 spaces and no TABs indenting.
    """

    spaces = 4

    def __init__(self, out):
        self.out = out
        self.indent = 0
        self.newline = 1
        self.lastws = (0, "")
        self.spacing = " " * self.spaces
        self.space_token = set(("=", "==", "<", ">", "!=", "<=", ">=","+=","-=","*=","/=","<<",">>"))

    def __emit(self, text):
        """ Write a piece of source code.
        """
        self.out.write(text)

    def __adjustIndent(self, idx):
        """ Calc adjusting offset for comments.

            Since the tokenizer emits INDENT/DEDENT only AFTER a series
            of COMMENTS, we need this helper.
        """
        from pythius import grok
        result = 0

        # add up any INDENTS or DEDENTS that follow COMMENTs
        while idx < len(self.parser.tokenlist):
            token = self.parser.tokenlist[idx]
            if token.type == grok.INDENT:
                result +=1
            elif token.type == grok.DEDENT:
                result -= 1
            elif token.type not in [grok.EMPTY, grok.WS, grok.COMMENT] or result:
                break
            idx += 1

        return result

    def parse(self, source):
        """ Parse Python source and emits a newly indented version of it.
        """
        from pythius import grok

        # the parser already detabs the source
        self.parser = grok.Parser()
        self.parser.parse(source)
        call_depth = 0

        # a dictionary of the whitespace seen last for a certain indent level
        wslevel = {0: 0}
        tokenlist_len = len(self.parser.tokenlist)
        token_pre = None
        # iterate over the list of tokens
        for idx in range(tokenlist_len):
            # get current token; note that getting the next token is
            # always ok in the code below since we always have "ENDMARKER"
            # following any token _before_ the end marker
            token = self.parser.tokenlist[idx]
            token_next = self.parser.tokenlist[idx+1] if idx < tokenlist_len-1 else None
            
            token_txt = token.text
            if token_txt == "(":
                call_depth+=1
            elif token_txt == ")":
                call_depth-=1
            
#            print "%s|"%token.text


            if _debug:
                import string, sys
                print >>sys.stderr, string.rjust(str(token.row), 5), string.rjust(str(token.col), 5), string.ljust(grok.tokentext[token.type], 10), repr(token.text)

            # end processing on ENDMARKER
            if token.type == grok.ENDMARKER: break

            # remember whether last token started a new line, and reset that flag
            isNewline = self.newline
            self.newline = 0

            # check token type and act accordingly
            if token.type == grok.INDENT:
                self.newline = 1
                self.indent += 1

                if self.parser.tokenlist[idx+1].type == grok.WS:
                    wslevel[self.indent] = len(self.parser.tokenlist[idx+1].text)
            elif token.type == grok.DEDENT:
                self.newline = 1
                self.indent -= 1
                self.lastws = (self.indent, ' ' * wslevel[self.indent])
            elif token.type in (grok.NEWLINE, grok.COMMENT):
                self.newline = 1
                self.__emit(token.text)
            elif token.type == grok.EMPTY:
                self.newline = 1
                self.__emit(token.text)
                self.lastws = (self.indent, ' ' * wslevel[self.indent])
            elif isNewline and token.type == grok.WS:
                if _debug:
                    import string, sys
                    print >>sys.stderr, "***", self.indent, self.__adjustIndent(idx)

                # check for adjustment if indenting seems fishy
                indent = self.indent
                cmadjust = 0
                if len(token.text) != wslevel[self.indent]:
                    # and self.parser.tokenlist[idx+1].type == grok.COMMENT:
                    adjust = self.__adjustIndent(idx)
                    indent += adjust
                    if adjust < 0 and self.parser.tokenlist[idx+1].type == grok.COMMENT:
                        if _debug:
                            import string, sys
                            print >>sys.stderr, self.parser.tokenlist[idx+1].text, "   ", indent, len(token.text), wslevel
                #while len(token.text) > wslevel[indent+cmadjust] and indent+cmadjust < self.indent:
                #    cmadjust += 1

                # emit canonical whitespace
                self.__emit(self.spacing * (indent+cmadjust))

                # keep manual additional indent of continued lines
                if _debug:
                    import string, sys
                    print >>sys.stderr, self.lastws[0], indent, len(self.lastws[1]), len(token.text), self.parser.tokenlist[idx+1].text
                if self.lastws[0] == indent and self.lastws[1] != token.text:
                    self.__emit(token.text[len(self.lastws[1]):])
                else:
                    self.lastws = (indent, token.text)
            elif token_next.text in self.space_token and token.text[-1] != ' ' and not call_depth:
                self.__emit(token.text+" ")
            elif token.text in self.space_token and token_next.text[0] != ' ' and not call_depth:
                self.__emit(token.text+" ")
            elif token.text == ",":
                if token_next.type != grok.NEWLINE and token_next.type != grok.EMPTY:
                    if token_next.type == grok.WS:
                        if token_next.text.isspace():
                            token_next.text = " "
                        else:
                            token_next.text = token_next.text.lstrip()
                    else:
                        token.text+=" "
                self.__emit(token.text)
            else:

                if not token_txt.strip():
                    if call_depth and ((token_pre and token_pre.text == '=') or (token_next and token_next.text == '=')):
                        token_txt = ''
                    elif ((token_pre and token_pre.text in self.space_token) or (token_next and token_next.text in self.space_token)):
                        token_txt = " "

                if token_txt:
                    self.__emit(token_txt)
            
            token_pre = token
#############################################################################
### Main program
#############################################################################

def usage():
    """ Print usage information.
    """
    import os, sys
    sys.stderr.write("""
%s v%s, Copyright (c) 2001 by Jgen Hermann <jh@web.de>

Usage: %s [options] [files...]

Options:
    -c, --compile           Compile reformatted source
    -n, --dry-run           Don't change any files on disk
    -q, --quiet             Be quiet (no informational messages)
    --no-backup             Don't make backups
    --help                  This help text
    --version               Version information

""" % ('pydent', __version__, 'pydent'))
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
    """ pydent's main code.
    """
    import getopt, sys, cStringIO, py_compile

    #
    # Check parameters
    #
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'cnq', ['compile', 'dry-run', 'help', 'quiet', 'no-backup', 'version'])
    except:
        util.fatal("Invalid parameters!", usage = 1)

    if util.haveOptions(optlist, ["--version"]): version()
    if not args or util.haveOptions(optlist, ["--help"]): usage()

    global flag_backup, flag_compile, flag_dryrun
    flag_backup = not util.haveOptions(optlist, ["--no-backup"])
    flag_compile = util.haveOptions(optlist, ["-c", "--compile"])
    flag_dryrun = util.haveOptions(optlist, ["-n", "--dry-run"])
    util.flag_quiet = util.haveOptions(optlist, ["-q", "--quiet"])

    #
    # Collect file names
    #
    files = []
    for name in args:
        files.extend(util.getFilesForName(name))
    util.log("Found %d file%s." % (len(files), ("", "s")[len(files) != 1], ))

    #
    # Process the files
    #
    for filename in files:
        # load source
        util.log("Formatting '%s'..." % (filename, ))
        file = util.FileMorpher(filename, backup = flag_backup, dryrun = flag_dryrun)
        source = file.load()

        # check source
        if not util.checkSource(source):
            util.log("Syntax errors in '%s', skipped." % (filename, ))
            continue

        # indent source
        stream = cStringIO.StringIO()
        indenter = Indenter(stream)
        indenter.parse(source)
        newsource = stream.getvalue()
        del stream
        del indenter

        # save if necessary
        if newsource != source:
            if not util.checkSource(newsource):
                # we produced an error in the formatted source
                open('error.dat', 'wt').write(newsource)
                util.fatal("INTERNAL ERROR: Bad formatting, see file 'error.dat'!")
            elif flag_dryrun:
                util.log("Would write %(new)d bytes (previously %(old)d bytes)." % {
                    'old': len(source), 'new': len(newsource), })
            else:
                # save new source
                util.log("Saving '%s'..." % (filename, ))
                file.save(newsource)

                # optionally compile it
                if flag_compile:
                    util.log("Compiling '%s'..." % (filename, ))
                    py_compile.compile(filename)
        del file


def run():
    global util
    from pythius import util
    util.runMain(main)


if __name__ == "__main__": run()

