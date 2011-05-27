__revision__ = "$Id: aop-unittests.py,v 1.18 2002/07/07 07:39:43 ftobin Exp $"

import unittest
import aop


class PointcutTest(unittest.TestCase):
    def setUp(self):
        self.logger = Logging()

    def make_student(self):
        self.student = make_aspected_student(self.logger)

    def make_studentsub(self):
        self.student = make_aspected_student(self.logger, False)

    def add_one_around(self, cxt):
        return cxt.proceed()+1



class GetattrTest(PointcutTest):
    type = 'getattr'

    def test_before(self):
        attr = 'age'
        self.logger.before(self.type, attr, self.logger.log)
        self.make_student()

        value = getattr(self.student, attr)

        cxt = self.logger.logged_cxt
        self.assertEquals(cxt['name'], attr)
        self.assert_(cxt['self'] is self.student)


    def test_after(self):
        attr = 'gpa'
        # get the value before we give advice
        orig_value = Student_defaults[attr]

        self.logger.after(self.type, attr, self.logger.log)

        self.make_student()

        # trigger the advice
        getattr(self.student, attr)

        cxt = self.logger.logged_cxt
        self.assertEquals(cxt['name'], attr)
        self.assertEquals(cxt['value'], orig_value)
        self.assert_(cxt['self'] is self.student)


    def test_around(self):
        attr = 'grade'

        orig_value = Student_defaults[attr]

        self.logger.around(self.type, attr, self.add_one_around)
        self.make_student()

        new_value = getattr(self.student, attr)

        self.assertEquals(orig_value+1, new_value)


class SetattrTest(PointcutTest):
    type = 'setattr'

    def test_before(self):
        attr = 'age'
        value = 3
        # just to make sure we're not setting it to what it
        # is already equal
        self.assertNotEquals(Student_defaults[attr], value)

        self.logger.before(self.type, attr, self.logger.log)

        self.make_student()
        setattr(self.student, attr, value)

        cxt = self.logger.logged_cxt
        self.assertEquals(cxt['name'], attr)
        self.assertEquals(cxt['value'], value)
        self.assertEquals(cxt['self'], self.student)
        self.assertEquals(getattr(self.student, attr), value)


    def test_after(self):
        attr = 'gpa'
        value = 3
        # just to make sure we're not setting it to what it
        # is already equal
        self.assertNotEquals(Student_defaults[attr], value)

        self.logger.after(self.type, attr, self.logger.log)

        self.make_student()
        setattr(self.student, attr, value)

        cxt = self.logger.logged_cxt
        self.assertEquals(cxt['name'], attr)
        self.assertEquals(cxt['value'], value)
        self.assertEquals(cxt['self'], self.student)
        self.assertEquals(getattr(self.student, attr), value)


    def test_around(self):
        attr = 'grade'
        value = 3
        # just to make sure we're not setting it to what it
        # is already equal
        self.assertNotEquals(Student_defaults[attr], value)

        self.logger.around(self.type, attr, self.no_change)

        self.make_student()
        setattr(self.student, attr, value)

        self.assertNotEquals(getattr(self.student, attr), value)


    def no_change(self, cxt):
        self.assert_(cxt['self'] is self.student)
        return


class MethodCallTest(PointcutTest):
    type = 'method_call'

    def test_before(self):
        method_name = 'add'
        varargs = (2, 3)
        kwargs       = {}

        self.logger.before(self.type, method_name, self.logger.log)

        self.make_student()
        apply(getattr(self.student, method_name), varargs, kwargs)

        cxt = self.logger.logged_cxt
        self.assertEquals(cxt['name'], method_name)
        self.assertEquals(cxt['varargs'], varargs)
        self.assertEquals(cxt['kwargs'], kwargs)

    def test_after(self):
        # note: we also test the kwargs here
        method_name = 'sub'
        varargs = ()
        kwargs       = {'b': 2, 'a': 3}

        self.logger.after(self.type, method_name, self.logger.log)

        self.make_student()
        rv = apply(getattr(self.student, method_name), varargs, kwargs)

        cxt = self.logger.logged_cxt
        self.assertEquals(cxt['name'], method_name)
        self.assertEquals(cxt['varargs'], varargs)
        self.assertEquals(cxt['kwargs'], kwargs)
        self.assertEquals(rv, kwargs['a'] - kwargs['b'])
        self.assertEquals(cxt['rv'], kwargs['a'] - kwargs['b'])

    def test_around(self):
        method_name = 'mul'
        varargs = (3, 2)
        kwargs = {}

        self.logger.around('method_call', method_name, self.add_one_around)

        self.make_student()
        rv = apply(getattr(self.student, method_name), varargs, kwargs)

        self.assertEquals(rv, 1+(reduce(lambda x, y: x*y, varargs)))



class InitTest(PointcutTest):
    type = 'init'
    init_record = 'initted'

    def test_before(self):
        self.logger.before(self.type, self.type, self.logger.log)

        self.make_student()
        cxt = self.logger.logged_cxt

        self.assert_(cxt['self'] is self.student)

    def test_after(self):
        self.logger.after(self.type, self.type, self.logger.log)

        self.make_student()

        cxt = self.logger.logged_cxt
        self.assert_(cxt['self'] is self.student)
        self.assert_(getattr(self.student, self.init_record))

    def test_subclasser_after(self):
        self.logger.after(self.type, self.type, self.logger.log)

        self.make_studentsub()

        cxt = self.logger.logged_cxt
        self.assert_(cxt['self'] is self.student)
        self.assert_(getattr(self.student, self.init_record))

    def test_around(self):
        null = lambda cxt: 0  # ensure the inits don't get called
        self.logger.around(self.type, self.type, null)

        self.make_student()

        self.assert_(not hasattr(self.student, self.init_record))


class AspectAddTest(PointcutTest):
    def setUp(self):
        PointcutTest.setUp(self)
        self.noter = Noting()

    def test_add(self):
        type = 'getattr'
        name = 'add'

        self.logger.before(type, name, self.logger.log)
        self.noter.before(type, name, self.noter.note)

        self.logger.extend(self.noter)

        student = make_aspected_student(self.logger)

        getattr(student, name)

        self.assertEquals(self.logger.logged_cxt['name'], name)
        self.assertEquals(self.noter.note, (self.noter.note_prefix + name))



class Logging(aop.Aspect):
    def __init__(self):
        self.logged_cxt = None
        super(Logging, self).__init__()

    def log(self, cxt):
        self.logged_cxt = cxt


class Noting(aop.Aspect):
    """Very similar to Logging but with different names
    and slightly different behaviour, so we
    can test things like aspect addition"""

    note_prefix = "note: "

    def __init__(self):
        self.note_cxt = {}
        super(Noting, self).__init__()

    def note(self, cxt):
        self.note = self.note_prefix + cxt['name']



# This is here so that these values can be read
# for the Student class while being locally
# close so they can be kept in sync easily.
Student_defaults = {'age': 16,
                    'gpa': 4,
                    'grade': 11}


def make_aspected_student(aspect, get_sub=False):

    class Student(object):
        __metaclass__ = aop.Metaclass
        _aspect = aspect

        # NOTE: if you change any of these, change
        # Student_defaults
        age        = 16
        grade = 11

        def __init__(self):
            self.initted = 1
            self.gpa = 4

        def add(self, a, b):
            return a+b

        def sub(self, a, b):
            return a-b

        def mul(self, a, b):
            return a*b

    class StudentSub(Student):
        def __init__(self):
            super(StudentSub, self).__init__(self)

    if get_sub:
        student = StudentSub()
    else:
        student = Student()

    return student




########################################################################

if __name__ == "__main__":
    unittest.main()
