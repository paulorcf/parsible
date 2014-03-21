__author__ = 'paulorcf'

import unittest
import re
from plugins.parsers import libxl
from plugins.processors import plibxl


class TestLibxlParsible(unittest.TestCase):
    """
    Tests related extract log from libXL.
    """

    def setUp(self):
        self.msg_correct = 'libxl: debug: libxl.c:1043:domain_death_xswatch_callback:  exists shutdown_reported=0 dominf.flags=ffff0020'
        self.msg_wrong = 'libxl: debug: libxl.c:1009:domain_death_xswatch_callback: [evg=0] all reported'
        pass


    def test_process_libxl(self):
        """
        I don't have anyway to get something from this method, only test IndexError, ValueError etc.
        """
        correct = libxl.parse_libxl(self.msg_correct)
        plibxl.process_api(correct)


    def test_parser_libxl_wrong_line(self):
        wrong = libxl.parse_libxl(self.msg_wrong)  # wrong line

        if 'status' in wrong.keys():
            self.fail("Error")
        else:
            self.assertTrue(True)  # force the green light :-P

    def test_parser_libxl(self):
        compare = (["status", "exists"],
                   ["libname", "libxl"],
                   ["loglevel", "debug"],
                   ["dominf", 'ffff0020'],
                   ["d_callback", "libxl.c:1043:domain_death_xswatch_callback"],
                   ["report_name", "shutdown"],
                   ["report_id", "0"])

        correct = libxl.parse_libxl(self.msg_correct)  # correct line

        for k, v in compare:
            if k in correct.keys():
                self.assertEqual(correct[k], v)
            else:
                self.fail("Key: %s not found" % k)


    def test_parser_libxl(self):
        compare = (["status", "exists"],
                   ["libname", "libxl"],
                   ["loglevel", "debug"],
                   ["dominf", '10004'],
                   ["d_callback", "libxl.c:1043:domain_death_xswatch_callback"],
                   ["report_name", "shutdown"],
                   ["report_id", "0"])

        correct = libxl.parse_libxl(self.msg_correct)  # correct line

        for k, v in compare:
            if k in correct.keys():
                self.assertEqual(correct[k], v)
            else:
                self.fail("Key: %s not found" % k)

    def test_regex_parser(self):
        parser_func = "(?P<libname>[\w\S]+)\s(?P<loglevel>[\w\S]+)\s(?P<d_callback>[\w\S]+)\s\s(?P<status>[\w\S]+)\s(?P<report>[\w\S]+)\s(?P<dominf>[\w\S]+)"

        line = self.msg_correct  # Correct line
        regex = re.compile(parser_func)
        r = regex.search(line)
        if r:
            for k, v in r.groupdict().iteritems():
                print (k + " " + v)

        dominf = r.group("dominf")
        self.assertEqual(dominf.split("=")[1], "10004")

        line = self.msg_wrong  # Wrong line
        regex = re.compile(parser_func)
        r = regex.search(line)
        print("Wrong line")
        if r:
            for k, v in r.groupdict().iteritems():
                if k == 'libname':
                    self.fail("Error parser, regex not fully correct")