from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import unittest, time, re
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Search(unittest.TestCase):
    
    def search(self):
        driver = self.driver
        driver.get(self.base_url + "file:///work/selenium/latest/anisha/index.html#")
        print "Verified results for:"
        with open("./data/json_data.json") as data_file:
            data_text = json.load(data_file)
            
            for each in data_text:  
                text = each["name"]
                driver.find_element_by_id("livefilter-input").clear()
                driver.find_element_by_id("livefilter-input").send_keys(text)
                driver.find_element_by_id("livefilter-input").send_keys(Keys.RETURN)
                highlights = driver.find_elements_by_class_name("hl")
                highlight_text =  {z.text.lower() for z in highlights}
                for h in highlight_text:
                    self.assertEqual(text, h,"Assertion failed")
                    print h

                time.sleep(1)
    
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
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

