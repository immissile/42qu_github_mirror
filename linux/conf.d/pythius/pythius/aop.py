from __future__ import nested_scopes
"""Aspect Oriented Programming toolkit

This module is a toolkit to help implement Aspect-Oriented
Programming techniques.  The usage concentrates on being able to
insert at run-time context-aware 'advice' for 'important' parts
of the program.  These 'important' parts of a program are
referred to as 'pointcuts'; examples of pointcuts for this
module are object attribute getting/setting, object initialization,
and method calls.

This documentation does not attempt to introduce one to
aspect oriented programming concepts.  For an overview, please see
http://www.aosd.org/

Here's a quick run-down of the way this module works if you are familiar
with the lingo:

1.  Create an Aspect.
2.  Define 'advice' for the Aspect.
3.  Define when the advice is applied (to what pointcuts).
4.  Set the __metaclass__ attribute of a class to aop.Metaclass
5.  Set the _aspect attribute of a class to an aop.Aspect instance
5.  Run the program as normal.

Now, we're going to run through that much more slowly, but not
the order described above, because the concepts are probably
better understood arranged in another order.  We'll work from the bottom
up.


POINTCUTS

A key concept is that of a 'pointcut'. A pointcut is an important
piece of the run-time program, a 'highlight' if you will.
This module defines the following types of pointcuts:

  *  getattr -- object attribute getting
  *  setattr -- object attribute setting
  *  init -- object initialization (not exactly the same as construction)
  *  method_call -- method running (applying a method, if you will)

Now that we've defined our types of pointcuts, the goal is to
define code which can be run near these pointcuts, and which
has a glimpse into the context of that pointcut.  We call
these bits of code 'advice'.  They are nothing more than
routines that accept a single parameter, a PointcutContext object.

And what might a Pointuct Context object tell us, you might ask?
Well, you're a little ahead of yourself, beecause we first
need to talk about the different 'timeframes' which pointcut
can run in.  You see, we want to be able to say 'run foo() after
the method bar() is run', and similar.  Here are the different
types of timeframes:

  * before -- right before the pointcut
  * after  -- you guessed it: right after the pointcut!
  * around -- 'surrounding' the pointuct.  We'll talk about
              this one more later.

For more details on the timeframes, see the documentation
for each one in the class Aspect.

Still with me?  Good.  We just have one more concept to introduce,
and then we're onto code.  The last concept is Aspects.


ASPECTS

Aspects in this module are nothing more than instances
of a class which inherits from the Aspect class, and have the
responsibility of 'affecting' classes with the advice you define.
An example might help make this clearer.  We'll define
a class Logger which prints some interesting information
about context when certain attributes are accessed:

>>> import aop
>>> 
>>> class Logger(aop.Aspect):
...     def __init__(self):
...         # Note that this is *extended*, not overriden...
...         super(Logger, self).__init__()  # so don't forget this!
... 
...         # After we do a getattr on the 'area' attribute, run
...         # self.log
...         self.after('getattr', 'area', self.log)
... 
...     def log(self, cxt):
...         value    = cxt['value']
...         name     = cxt['name']
...         print 'Accessed attribute %s (value of %s)' % (name, value)
... 
>>> 
>>> my_logger = Logger()
>>> 
>>> class Square:
...     __metaclass__ = aop.Metaclass    # This is constant!
...
...     # This changes!  Note that we are referring to an *instance*
...     # of an Aspect, not the Logger class itself.
...     _aspect = my_logger
... 
...     def __init__(self, x):
...         self.x = x
...         self.area = x*x  # We'll assume the square is immutable
... 
>>> 
>>> my_square = Square(4)
>>> print 'The square has sides of length %d' % my_square.x
The square has sides of length 4
>>> 
>>> print 'The square has an area of size %d' % my_square.area
Accessed attribute area (value of 16)
The square has an area of size 16

See that second-to-last output line?  That's our 'after/getattr'
advice running.  It runs right after we access the 'area'
attribute for our my_square object.


CONTEXT INFORMATION

A few notes now.  You're probably still wondering what that cxt
thing passed into the Logging.log() method was.  Well, it's
merely a PointcutContext dictionary, with keys/values describing
the context the pointcut is running in.  The keys that are filled
in depend on the type of pointuct you are giving advice for.

Each advice routine must accept one argument, and it will be
one of these PointcutContext arguments (or a subclass thereof).

Here is a table describing the different types of context information
given.

Possible PointcutContext keys and their meaning:

  * timeframe - is this before/after/point, etc
  * type      - getattr/setattr/method_call etc
  * name      - The 'name' of the highlighted pointcut, which
                varies.  For getattr/setattr, it is the
                attribute name.  For a method_call, it is
                the method's name.  For an init, it is
                just the word 'init'.
  * self      - The object relevant to the situation.
                For example, the object which is being setattr'd
  * value     - For setattr and getattr, the value of the attribute
  * rv        - Return value of the method call
  * varargs   - A list of method non-keyword arguments
  * kwargs    - A dictionary of method keyword arguments
  * method    - The method being executed


Here is another table which describes which types and
timeframes of pointcuts have which PointcutContext keys.
Note that *every* PointcutContext has the keys 'type', 'timeframe',
and 'name'.

  * getattr (before)        - self, name
  * getattr (after)/setattr - self, name, value
  * method_call (before)    - method, varargs, kwargs
  * method_call (after)     - (same as before), rv
  * init                    - self

The 'around' timeframe receives the same context as 'before'.

If you ever forget what context information you get for a
type of type+timeframe, just peer into the PointcutContext
argument's keys; after all, it's just a dictionary!

Enough with tables.  They bore you and me, but we need them for
reference.

Don't mess around with the contexts; treat them as read-only.
Or else your code might hurt you.


THE AROUND TIMEFRAME

The 'around' timeframe I left it out until now, because it's a
little different and a tad more complex, but mainly because it's
a neat little gizmo. 'around' advice 'surrounds' a pointcut, and is
both before and after it.  You entirely encapsulate the pointcut,
and can even prevent it from happening altogether!  Here's a little
example:

>>> import aop
>>> 
>>> class OffByOne(aop.Aspect):
...     def __init__(self):
...         # Note that this is *extended*, not overriden...
...         super(OffByOne, self).__init__()  # so don't forget this!
...         
...         # When an 'add' method is called, surround it with
...         # our 'bump_up_one' method.
...         self.around('method_call', 'add', self.bump_up_one)
...     
...     def bump_up_one(self, cxt):
...         "Have the routine return one more than it naturally does"
...         # Calling 'proceed' here causes the next 'layer'
...         # of 'arounds' to execute.  Since we're only applying
...         # one 'around', wrapper, this calls the 'real'
...         # method that we're surrounding.
...         rv = cxt.proceed()
...         return rv + 1
... 
>>> 
>>> obo = OffByOne()
>>> 
>>> class Student(object):
...     __metaclass__ = aop.Metaclass    # This is constant!
...     
...     # This changes!  Note that we are referring to an *instance*
...     # of an Aspect, not the OffByOne class itself.
...     _aspect = obo
...     
...     def add(self, a, b):
...         return a+b
... 
>>> student = Student()
>>> 
>>> print student.add(2, 2)
5

We now have proof that 2+2 is 5.  After all, computers don't make
mistakes. :)

What the proceed() did was to cause the 'surrounded' pointcut
to execute, and we then modified its output (and returned it
like the method would have).  We basically 'substitute' for
the thing we are 'around' (in this case, the add() method).

Note:  you don't have to call proceed(); we could have just had
it so that add() always returned the constant '5'
if we wanted, without adding 1 to the rv after it was calculated.


MULTIPLE ADVICE RESOLUTION

If multiple pieces of advice apply to a pointcut type+timeframe
context, then the order in which they were given to the
Aspect via before() or after() is the order they are run in.

In constrast, Around advice can be thought of as nested.  Each layer
given to the aspect via around() creates another outer layer,
wrapping around the inner layers.  When a proceed() happens
during advice for an outer layer, it starts calling the advice
for the inner layer.  Note that not calling proceed() results
in the nest-inner layer of advice not running.


ASPECT COMBINATION

It's very likely you'll want to apply multiple aspects to a class.
The best way to do this is to 'add' aspects together before
having them 'affect' the target class.  For example:

logging = Logging()
tracing = Tracing()

logging.extend(tracing)


TROUBLESHOOTING

You *must* define __metaclass__ in your 'affected' class to be
aop.Metaclass this is the magic trigger.

If you define '__metaclass__ = aop.Metaclass' for a class, you *must*
set '_aspect' for that class to be an aop.Aspect (or subclass) instance.

Don't forget to call the Aspect.__init__ in your aop.Aspect'-inheriting
subclass's constructor.


LICENSE:

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
or see http://www.gnu.org/copyleft/lesser.html
"""

__author__         = "Frank J. Tobin, ftobin@neverending.org"
__revision__ = "$Id: aop.py,v 1.35 2002/07/08 03:52:09 ftobin Exp $"


import new
import inspect


class Metaclass(type):
    def __init__(self, name, bases, dikt):
        super(Metaclass, self).__init__(name, bases, dikt)

        self.__klass_name = name

        if not hasattr(self, '_aspect'):
            raise RuntimeError,\
                  "class %s does not an '_aspect' specified" % name

        # this is just to have an anonymous, empty Aspect
        # if the user doesn't set one
        self.__backup_getattrs()
        self.__load_Instance_dict()


    def __load_Instance_dict(self):
        for (k, v) in Instance.__dict__.items():
            if k == '__init__':
                self._backup_dict[k] = getattr(self, k)

            if inspect.isfunction(v):
                setattr(self, k, new.instancemethod(v, None, self))


    def __backup_getattrs(self):
        self._backup_dict = {}
        self._aspect.lock()

        for name in self._aspect.affected_getattrs():
            if hasattr(self, name):
                self._backup_dict[name] = getattr(self, name)
                delattr(self, name)


class Aspect(object):
    __slots__ = ['_pc_advice', '__locked', '_affected_getattrs']
    pc_timeframes = ('after', 'before', 'around')
    pc_types            = ('getattr', 'setattr', 'method_call', 'init')

    def __init__(self):
        self._pc_advice = {}
        self.__locked = False
        self._affected_getattrs = None

        # just some datastructure rearranging for computer eyes
        # instead of human eyes like it's declared in the class
        for type in self.pc_types:
            self._pc_advice[type] = {}
            for timeframe in self.pc_timeframes:
                self._pc_advice[type][timeframe] = {}


    def lock(self):
        if self._affected_getattrs is None:
            self.__set_affected_getattrs()
        self.__locked = True


    def _at(self, timeframe, type, name, routine):
        """Define advice that is run at timeframe/type.

        timeframe can be one of:
        ('before', 'after', 'around')

        type can be one of:
        ('getattr', 'setattr', 'method_call', 'init')

        pattern is a regular expression pattern that
        is used to match the 'name' portion of contexts.
        
        routine is a callable object, such as a method or function.
        It must have the signature of receiving one argument
        (or two if it is a bound method).  This argument
        will be a PointuctContext object.
        """
        if self.__locked:
            raise RuntimeError,\
                  "cannot modify an Aspect after used for a Metaclass"""

        if type not in self.pc_types:
            raise ValueError, "invalid pointcut type: %s" % type
        if timeframe not in self.pc_timeframes:
            raise ValueError, "invalid pointcut timeframe: %s" % type

        self._pc_advice[type][timeframe].setdefault(name, []).append(routine)


    def before(self, type, name, routine):
        """Thin wrapper over _at().  Will run
        routine() after any pointcut of type 'type'
        that matches the regular exrpession 'name'.

        See _at() for more details.
        """
        self._at('before', type, name, routine)


    def after(self, type, name, routine):
        """Thin wrapper over _at().  Will run
        routine() after any pointcut of type 'type'
        that matches the regular exrpession 'name'.

        See _at() for more details.
        """
        self._at('after', type, name, routine)


    def around(self, type, name, routine):
        """Thin wrapper over _at().  Will run
        routine() around any pointcut of type 'type'
        that matches the regular exrpession 'name'.
        
        The routine() will receive an AroundContext
        object, which implements proceed().
        By not calling proceed() on the context object,
        one can prevent the 'core' of the pointcut
        from executing.

        The return value from the routine will be returned
        to the calling context.

        See _at() for more details.
        """
        self._at('around', type, name, routine)


    def __set_affected_getattrs(self):
        if self.__locked:
            raise RuntimeError, "cannot modify Aspect while locked"

        names = []
        for type in ('getattr', 'method_call'):
            for timeframe in self.pc_timeframes:
                names.extend(self._pc_advice[type][timeframe].keys())

        self._affected_getattrs = names


    def affected_getattrs(self):
        if not self.__locked:
            raise RuntimeError, "affected getattrs not settled until locked"
        return self._affected_getattrs


    def _routines(self, cxt):
        """Return a list of routines that the user
        has defined as wanting to be run at PointcuContext cxt.
        """

        type            = cxt['type']
        timeframe = cxt['timeframe']
        name            = cxt['name']

        return self._pc_advice[type][timeframe].get(name, [])


    def apply_routines(self, cxt):
        """Run the routines applicable to context cxt"""
        for r in self._routines(cxt):
            apply(r, (cxt, ))


    def extend(self, other):
        """Return new aspect which combines the advice of
        the left and right aspects."""

        for (type, type_branch) in other._pc_advice.items():
            for (timeframe, timeframe_branch) in type_branch.items():
                for (name, routines) in timeframe_branch.items():
                    self._pc_advice[type][timeframe].setdefault(name, []).extend(routines)



class Instance(object):
    """We just use the attributes of this class to override
    any classes we 'affect' with Metaclass"""
    def __init__(self, *varargs, **kwargs):
        # our private namespace
        # it differs from the class var, _backup_dict
        # since if the user does setattrs, we don't
        # want it affectint the class, only our stuff
        self.__ns = {}

        cxt = PointcutContext({ 'timeframe': 'before',
                                'type':      'init',
                                'name':      'init',
                                'self':      self,
                                })
        self._aspect.apply_routines(cxt)

        cxt['timeframe'] = 'around'
        AroundContext(cxt, self._aspect,
                      self.__init_core, varargs, kwargs).proceed()

        cxt['timeframe'] = 'after'
        self._aspect.apply_routines(cxt)


    def __init_core(self, *varargs, **kwargs):
        # Sometimes __init__ isn't defined for a class.
        # It isn't defined for old-style classes, which
        # we should still support for a while, since many
        # modules use them.
        if self._backup_dict.has_key('__init__'):
            method = self._backup_dict['__init__']
            apply(method, ((self, )+varargs), kwargs)
    # remember, init returns nothing

    def __getattr__(self, name):
        cxt = PointcutContext({ 'timeframe': 'before',
                                'type':      'getattr',
                                'name':      name,
                                'self':      self,
                                })

        self._aspect.apply_routines(cxt)

        cxt['timeframe'] = 'around'
        value = AroundContext(cxt, self._aspect,
                              self.__getattr_core, (name, ), {}).proceed()

        cxt['timeframe'] = 'after'
        cxt['value']           = value
        self._aspect.apply_routines(cxt)
        return value


    def __getattr_core(self, name):
        try:
            # Look in our private namespace first
            value = self.__ns[name]
        except KeyError:
            try:
                # now check anything we might have saved
                # from the class
                value = self._backup_dict[name]
            except KeyError:
                # Since we know that we did a delattr
                # on all attrs that we care about,
                # and any setattrs would go into into our private
                # namespace, then we can't have this attribute
                raise AttributeError, name

        if inspect.ismethod(value):
            value = BoundMethod(self, value, self._aspect)

        return value


    def __setattr__(self, name, value):
        cxt = PointcutContext({ 'timeframe': 'before',
                                'type':      'setattr',
                                'name':      name,
                                'self':      self,
                                'value':     value,
                                })

        self._aspect.apply_routines(cxt)

        cxt['timeframe'] = 'around'
        AroundContext(cxt, self._aspect,
                      self.__setattr_core, (name, value), {}).proceed()

        cxt['timeframe'] = 'after'
        self._aspect.apply_routines(cxt)


    def __setattr_core(self, name, value):
        """This is what really does the setting of attributes"""

        if name in self._aspect._affected_getattrs \
               and name != '_Instance__ns':
            d = self.__ns
        else:
            d = self.__dict__

        d[name] = value



class BoundMethod(object):
    __slots__ = ['im_class', 'im_self', 'im_func', '__name__',
                 '_aspect']

    def __init__(self, instance, method, aspect):
        self.im_class = method.im_class
        self.im_self        = instance
        self.im_func        = method.im_func
        self.__name__ = method.__name__
        self._aspect        = aspect

    def __call__(self, *varargs, **kwargs):
        cxt = PointcutContext({ 'timeframe': 'before',
                                'type':      'method_call',
                                'name':      self.__name__,
                                'method':    self,
                                'varargs':   varargs,
                                'kwargs':    kwargs,
                                })
        self._aspect.apply_routines(cxt)

        cxt['timeframe'] = 'around'
        around = AroundContext(cxt, self._aspect,
                               self.im_func,
                               ((self.im_self, ) + varargs),
                               kwargs)
        rv = around.proceed()

        cxt.update({'timeframe': 'after',
                    'rv': rv})
        self._aspect.apply_routines(cxt)
        return rv


class PointcutContext(dict):
    pass


class AroundContext(PointcutContext):
    __slots__ = ['routines', 'core']
    def __init__(self, routines_dict, aspect, core, varargs, kwargs):
        PointcutContext.__init__(self, routines_dict)
        self.routines = aspect._routines(routines_dict)
        self.core          = core
        self.varargs = varargs
        self.kwargs        = kwargs

    def proceed(self):
        """Execute the next 'layer' of 'around' wrapping,
        possibly ending up running the 'core' of the pointcut."""

        if len(self.routines) == 0:
            return apply(self.core, self.varargs, self.kwargs)

        r = self.routines.pop()
        return apply(r, (self, ))


def _run_doctests():
    import doctest, aop
    return doctest.testmod(aop)

if __name__ == '__main__':
    _run_doctests()
