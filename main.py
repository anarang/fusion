#!/usr/bin/env python
from selenium import webdriver
from lib.filter import Filter
from lib.search import Search
from lib.report_description import description
import os.path, unittest, argparse
import textwrap,sys
from time import strftime
from lib.HTMLTestRunner import HTMLTestRunner
from ConfigParser import ConfigParser
conf_file = open('config.conf')
config = ConfigParser()
config.readfp(conf_file)

class SampleTests(Filter, Search):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()        
        set_base_url = config.get("set_url",'url')
        self.base_url = set_base_url
        self.verificationErrors = []
     
    def test_search(self):
        self.search()
        
    def test_filter(self):
        self.filter_label()

    def tearDown(self):
        self.driver.quit()
        
search_case = unittest.TestSuite()
search_case.addTest(SampleTests('test_search'))

filter_case = unittest.TestSuite()
filter_case.addTest(SampleTests('test_filter'))

all_tests = unittest.TestSuite([search_case,filter_case])

parser = argparse.ArgumentParser(
    prog='main',
    version='flamingo 1.0',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description = textwrap.dedent('''\
         Sample test cases for search and filter
         Options: filter_case, search_case
         '''),
    add_help = True)

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('-t','--testcase',metavar='',help= "Execute individual Scripts based on the options mentioned above", choices=['search_case','filter_case'])
group.add_argument('-a','--all',action='store_true', help= "Run all the test scripts simultaneously")
suite = parser.parse_args()

if suite.all:
    suite.all='all_tests'
    print " Running all test cases as a suite"
    TESTCASE = suite.all
elif suite.testcase:
    print("Running %s test case "%suite.testcase)
    TESTCASE= suite.testcase
else:
    print("Please refer help")
    parser.print_version()
    parser.print_help()
    sys.exit(1)
        
report_format = strftime("%Y%m%d%H%M")       
reports_path = config.get("set_reports_path",'report_folder')
if not os.path.exists(reports_path):
    os.makedirs(reports_path)
outfile = open(os.path.join(reports_path,"report_%s_%s.html" % (TESTCASE, report_format)), 'w')

runner = HTMLTestRunner(stream= outfile, title='Test Report',description=description[TESTCASE])

try:
    if __name__ == "__main__":
        runner.run(eval(TESTCASE))
except KeyboardInterrupt:
    print("\nKeyboard Interrupt! No reports generated.")
            
