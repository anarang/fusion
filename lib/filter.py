from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, os
from ConfigParser import ConfigParser
conf_file = open('config.conf')
config = ConfigParser()
config.readfp(conf_file)
logs_path = config.get("set_logs_path",'log_folder')
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
import logging
if not os.path.exists(logs_path):
        os.makedirs(logs_path)
        open(os.path.join(logs_path,"log_file_%s.log"%datetime.date.today()),'a').close()
        logging.basicConfig(filename=os.path.join(logs_path,"log_file_%s.log"%datetime.date.today()),format=FORMAT, filemode='a', level=logging.INFO)


class Filter(unittest.TestCase):
    
    def filter_label(self):
        driver = self.driver
        driver.get(self.base_url + "")
        time.sleep(1)
        label1 = driver.find_element_by_xpath("//li[2]/label")
        label1.click()
        label1_text = label1.text
        print "Label selected for filter: ", label1_text
        logging.info("hello")
        time.sleep(2)
        element = driver.find_elements_by_class_name("title")
        element_text = [x.text for x in element]
        filtered_array = []
        regexp= r"[A-Za-z0-9]+" 
        for f in element_text:
            if re.match(regexp,f):
                filtered_array.append(f)
        for filtered in filtered_array:
            self.assertEqual(label1_text, filtered, "Filter does not work properly")
        print "Filter verified"

    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
