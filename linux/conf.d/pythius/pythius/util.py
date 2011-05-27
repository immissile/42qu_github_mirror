"""
    Pythius - Utility Functions

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

    $Id: util.py,v 1.1 2001/11/05 22:34:03 jhermann Exp $
"""
__version__ = "$Revision: 1.1 $"[11:-2]

# Imports
import os, sys

# Globals
flag_quiet = 0


#############################################################################
### Misc helpers
#############################################################################

def containsAny(str, set):
    """ Check whether 'str' contains ANY of the chars in 'set'
    """
    return 1 in [c in str for c in set]


#############################################################################
### Logging
#############################################################################

def fatal(msgtext, **kw):
    """ Print error msg to stderr and exit.
    """
    sys.stderr.write("FATAL ERROR: " + msgtext + "\n")
    if kw.get('usage', 0):
        maindict = vars(sys.modules['__main__'])
        if maindict.has_key('usage'):
            maindict['usage']()
    sys.exit(1)


def log(msgtext):
    """ Optionally print error msg to stderr.
    """
    if not flag_quiet:
        sys.stderr.write(msgtext + "\n")


#############################################################################
### Commandline Support
#############################################################################

def cmdInit():
    """ Common command initialization.
    """
    import time

    global _start_time
    _start_time = time.clock()


def runMain(mainloop):
    """ Run the main function of a command.
    """
    showtime = 1
    try:
        try:
            cmdInit()
            mainloop()
        except KeyboardInterrupt:
            log("*** Interrupted by user!")
        except SystemExit:
            showtime = 0
            raise
    finally:
        if showtime: logRuntime()


def logRuntime():
    """ Print the total command run time.
    """
    import time
    log("Needed %.3f secs." % (time.clock() - _start_time, ))


def haveOptions(optlist, options):
    """ Check whether one of the options in "options" is in the list of
        options ("optlist") created from the command line
    """
    return filter(lambda flag, o=options: flag[0] in o, optlist) != []


def getOption(optlist, options):
    """ Get the value of the options in "options", from the list of
        options ("optlist") created from the command line
    """
    match = filter(lambda flag, o=options: flag[0] in o, optlist)
    if match:
        return match[-1][1]
    else:
        return ""


def getOptionList(optlist, options):
    """ Get all the values of the options in "options", from the list of
        options ("optlist") created from the command line
    """
    opts = filter(lambda flag, o=options: flag[0] in o, optlist)
    return map(lambda o: o[1], opts)


#############################################################################
### File Handling
#############################################################################

def replaceFile(oldname, newname):
    """ Rename file 'oldname' to 'newname'.
    """
    if os.name == 'nt' and os.path.exists(oldname):
        # POSIX rename does an atomic replace, WIN32 rename does not. :-(
        try:
            os.remove(newname)
        except OSError, exc:
            import errno
            if exc.errno != errno.ENOENT: raise exc

    # rename it
    os.rename(oldname, newname)
    ##print "%s ==> %s" % (oldname, newname)


class FileMorpher:
    """ A class that enables a client to securely update an existing file,
        including the ability to make an automated backup version.
    """

    def __init__(self, filename, **kw):
        """ The constructor takes the filename and some options.

            backup -- boolean indicating whether you want a backup file
                (default is yes)
            dryrun -- don't actually change the file
        """
        self.filename = filename
        self.do_backup = kw.get('backup', 1)
        self.dryrun = kw.get('dryrun', 0)

        self.stream = None
        self.basename, ext = os.path.splitext(self.filename)


    def __del__(self):
        if self.stream:
            # Remove open temp file
            self.__close()
            if not self.dryrun:
                os.remove(self.__tempfile())


    def __tempfile(self):
        return self.basename + ".tmp"


    def __close(self):
        """ Close temp stream, if open.
        """
        if self.stream:
            self.stream.close()
            self.stream = None


    def load(self):
        """ Load the content of the original file into a string and
            return it. All I/O exceptions are passed through.
        """
        file = open(self.filename, "r")
        try:
            content = file.read()
        finally:
            file.close()

        return content


    def save(self, content):
        """ Save new content, using a temporary file.
        """
        file = self.opentemp()
        file.write(content)
        self.commit()


    def opentemp(self):
        """ Open a temporary file for writing and return an open stream.
        """
        assert not self.stream, "Write stream already open"

        if self.dryrun:
            import cStringIO
            self.stream = cStringIO.StringIO()
        else:
            self.stream = open(self.__tempfile(), "w")

        return self.stream


    def commit(self, **kw):
        """ Close the open temp stream and replace the original file,
            optionally making a backup copy.

            Options:
                getcontent -- return new file content, if true
        """
        assert self.stream, "Write stream not open"

        # dryrun mode?
        if self.dryrun:
            content = None
            if kw.get('getcontent', 0):
                content = self.stream.getvalue()
            self.__close()
            return content

        # close temp file
        self.__close()

        # do optional backup and rename temp file to the correct name
        if self.do_backup:
            replaceFile(self.filename, self.basename + ".bak")
        replaceFile(self.__tempfile(), self.filename)

        # optionally return new content
        if kw.get('getcontent', 0):
            return self.load()


#############################################################################
### Python Magic
#############################################################################

def checkSource(codestring):
    """ Compile a piece of python source, to check for syntax errors.

        Return true for valid source, false otherwise.
    """
    # canonicalize the line ends
    codestring = codestring.replace("\r\n", "\n")
    codestring = codestring.replace("\r", "\n")
    if codestring and codestring[-1] != '\n':
        codestring = codestring + '\n'

    # try to compile it
    try:
        codeobject = compile(codestring, '<syntaxcheck>', 'exec')
    except SyntaxError:
        return 0

    return 1


def _visit_pyfiles(list, dirname, names):
    """ Helper for getFilesForName().
    """
    # get extension for python source files
    if not globals().has_key('_py_ext'):
        import imp
        global _py_ext
        _py_ext = [triple[0] for triple in imp.get_suffixes() if triple[2] == imp.PY_SOURCE][0]

    # don't recurse into CVS directories
    if 'CVS' in names:
        names.remove('CVS')

    # add all *.py files to list
    list.extend(
        [os.path.join(dirname, file)
            for file in names
                if os.path.splitext(file)[1] == _py_ext])


def _get_modpkg_path(dotted_name, pathlist=None):
    """ Get the filesystem path for a module or a package.

        Return the file system path to a file for a module,
        and to a directory for a package. Return None if
        the name is not found, or is a builtin or extension module.
    """
    import imp

    # split off top-most name
    parts = dotted_name.split('.', 1)

    if len(parts) > 1:
        # we have a dotted path, import top-level package
        try:
            file, pathname, description = imp.find_module(parts[0], pathlist)
            if file: file.close()
        except ImportError:
            return None

        # check if it's indeed a package
        if description[2] == imp.PKG_DIRECTORY:
            # recursively handle the remaining name parts
            pathname = _get_modpkg_path(parts[1], [pathname])
        else:
            pathname = None
    else:
        # plain name
        try:
            file, pathname, description = imp.find_module(dotted_name, pathlist)
            if file: file.close()
            if description[2] not in [imp.PY_SOURCE, imp.PKG_DIRECTORY]:
                pathname = None
        except ImportError:
            pathname = None

    return pathname


def getFilesForName(name):
    """ Get a list of module files for a filename, a module or package name,
        or a directory.
    """
    import imp

    if not os.path.exists(name):
        # check for glob chars
        if containsAny(name, "*?[]"):
            import glob
            files = glob.glob(name)
            list = []
            for file in files:
                list.extend(getFilesForName(file))
            return list

        # try to find module or package
        name = _get_modpkg_path(name)
        if not name:
            return []

    if os.path.isdir(name):
        # find all python files in directory
        list = []
        os.path.walk(name, _visit_pyfiles, list)
        return list
    elif os.path.exists(name):
        # a single file
        return [name]

    return []


#
# Test code
#
if __name__ == "__main__":
    print 'exceptions =', _get_modpkg_path('exceptions')
    print 'spam =', _get_modpkg_path('spam')
    print 'httplib =', _get_modpkg_path('httplib')
    print 'xml =', _get_modpkg_path('xml')
    print 'xml.dom =', _get_modpkg_path('xml.dom')
    print 'xml.dom.minidom =', _get_modpkg_path('xml.dom.minidom')

