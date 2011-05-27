"""
    Pythius - Groking Python Source
    All rights reserved, see LICENSE for details.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    $Id: grok.py,v 1.1 2001/11/05 22:34:03 jhermann Exp $
"""
__version__ = "$Revision: 1.1 $"[11:-2]

# Imports
import string, sys, cStringIO
import keyword, token, tokenize


#############################################################################
### Python Source Tokenizer / Parser
#############################################################################

# our token types
KEYWORD          = token.NT_OFFSET + 1
TEXT             = token.NT_OFFSET + 2
WS               = token.NT_OFFSET + 3
NUMBER           = token.NUMBER
OP               = token.OP
STRING           = token.STRING
COMMENT          = tokenize.COMMENT
NAME             = token.NAME
ERRORTOKEN       = token.ERRORTOKEN
ENDMARKER        = token.ENDMARKER
INDENT           = token.INDENT
DEDENT           = token.DEDENT
NEWLINE          = token.NEWLINE
EMPTY            = tokenize.NL

tokentext = {
    KEYWORD: 'KEYWORD',
    TEXT: 'TEXT',
    WS: 'WS',
    NUMBER: 'NUMBER',
    OP: 'OP',
    STRING: 'STRING',
    COMMENT: 'COMMENT',
    NAME: 'NAME',
    ERRORTOKEN: 'ERRORTOKEN',
    ENDMARKER: 'ENDMARKER',
    INDENT: 'INDENT',
    DEDENT: 'DEDENT',
    NEWLINE: 'NEWLINE',
    EMPTY:   'EMPTY',
}


class ParseError(Exception):
    pass


class Token:

    def __init__(self, **kw):
        self.__dict__.update(kw)


class Parser:
    """ Parse python source.
    """

    def parse(self, source):
        """ Parse and send the colored source.
        """
        self.source = string.expandtabs(source)
        self.tokenlist = []

        # store line offsets in self.offset
        self.offset = [0, 0]
        self.lines = 0
        pos = 0
        while pos < len(self.source):
            self.lines = self.lines + 1
            pos = string.find(self.source, '\n', pos) + 1
            if not pos: break
            self.offset.append(pos)
        self.offset.append(len(self.source))

        # parse the source
        self.pos = 0
        text = cStringIO.StringIO(self.source)
        try:
            tokenize.tokenize(text.readline, self)
        except tokenize.TokenError, ex:
            msg = ex[0]
            line = ex[1][0]
            raise ParseError("ERROR %s\n%s" % (
                msg, self.source[self.offset[line]:]))


    def __push(self, toktype, toktext, srow, scol, line):
        self.tokenlist.append(Token(type=toktype, text=toktext, row=srow, col=scol, line=line))


    def __call__(self, toktype, toktext, (srow, scol), (erow, ecol), line):
        """ Token handler.
        """
        if 0: print "type", toktype, token.tok_name[toktype], "text", toktext,\
                    "start", srow, scol, "end", erow, ecol, "<br>"

        # calculate new positions
        oldpos = self.pos
        newpos = self.offset[srow] + scol
        self.pos = newpos + len(toktext)

        # handle newlines
        if toktype in [token.NEWLINE, tokenize.NL]:
            self.__push(toktype, '\n', srow, scol, line)
            return

        # send the original whitespace, if needed
        if newpos > oldpos:
            #!!! srow scol is the ENDING position here!
            self.__push(WS, self.source[oldpos:newpos], srow, scol, line)

        # skip indenting tokens
        if toktype in [token.INDENT, token.DEDENT]:
            self.pos = newpos
            self.__push(toktype, '', srow, scol, line)
            return

        # map token type to one of ours
        if token.LPAR <= toktype and toktype <= token.OP:
            toktype = OP
        elif toktype == token.NAME and keyword.iskeyword(toktext):
            toktype = KEYWORD

        if not tokentext.has_key(toktype): toktype = TEXT

        # add token
        self.__push(toktype, toktext, srow, scol, line)


if __name__ == "__main__":
    import os, sys

    # open own source
    source = open('grok.py').read()

    # parse it
    parser = Parser()
    parser.parse(source)

    # print it
    if 0:
        for tok in parser.tokenlist:
            print string.rjust(str(tok.row), 5), string.rjust(str(tok.col), 5),\
                  string.ljust(tokentext[tok.type], 10), repr(tok.text)

    # print stats
    def _stats(label, *args):
        print string.ljust(label, 20), string.join(map(str, args), '')

    def _count(toktype, p = parser):
        return len(filter(lambda x, t=toktype: x.type == t, p.tokenlist))

    _stats("Characters", len(parser.source))
    _stats("Lines", parser.lines)
    _stats("Comments", _count(COMMENT))
    _stats("Empty lines", _count(EMPTY))
    _stats("Classes", len(filter(lambda t: t.type == KEYWORD and t.text == "class", parser.tokenlist)))

