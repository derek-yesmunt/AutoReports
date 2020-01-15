from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time, os, fnmatch, shutil
import yagmail_send

t = time.localtime()
timestamp = time.strftime('%b-%d-%Y_%H%M', t)
shorttime = time.strftime('%b-%d-Y', t)

user = 'user'
pwd = 'password'

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver', options=options)
driver.get('https:www.autosite.com')
driver.find_element_by_id('logonBtn').click()
elem = driver.find_element_by_id('ctl00_ContentPlaceHolder1_UsernameTextBox')
elem.send_keys(user)
elem = driver.find_element_by_id('ctl00_ContentPlaceHolder1_PasswordTextBox')
elem.send_keys(pwd)
elem.submit()

nafta = driver.find_element_by_id("tln_firstLevel").find_element_by_link_text('Region').click()
applications = driver.find_element_by_id("tln_secondLevel").find_element_by_link_text('Apps').click()
##time.sleep(10)##
#seq = driver.find_elements_by_tag_name('iframe')#
#print("No of frames present in the web page are: ", len(seq))#
driver.switch_to.frame("ivuFrm_page0ivu2")
gpsis = driver.find_element_by_id('aaaa.SelectApp.AppName_editor.9').click()
time.sleep(5)

#Switch to new tabf#
driver.switch_to.window(driver.window_handles[1])

#Gpsis navagation#
driver.switch_to.frame("left")
purchase_order = driver.find_element_by_name('folder1261').click()
po_inquiry = driver.find_element_by_name('menu1423').click()

driver.switch_to.default_content()
driver.switch_to.frame("right")
driver.find_element_by_class_name("tdsidetitle3")

selectSupplier = Select(driver.find_element_by_name('supplierList'))
selectSupplier.select_by_visible_text('code')

#Set Report
selectReport = Select(driver.find_element_by_name('reportNamesDropDown'))
selectReport.select_by_value('0')
#vlaue 0 = Indirect PO List
#value 1 = Direct PO List
#value 2 = Tool PO LIst
#value 3 = Legacy Direct PO List
#value 4 = Legacy Indirect PO List


#Set Report Length
selectReport = Select(driver.find_element_by_name('pageRec'))
selectReport.select_by_value('2')
#value 0 = 25
#value 1 = 50
#value 2 = All

#Generate Report
driver.find_element_by_name('returnVal').click()
time.sleep(5)
INDIRECT_REPORT_NAME = ("Indirect PO's - " + timestamp + ".png")
driver.save_screenshot(INDIRECT_REPORT_NAME)

#Select Direct PO List
selectReport = Select(driver.find_element_by_name('reportNamesDropDown'))
selectReport.select_by_value('1')

#Set Report Length
selectReport = Select(driver.find_element_by_name('pageRec'))
selectReport.select_by_value('2')

#Generate Report
driver.find_element_by_name('returnVal').click()
time.sleep(5)
DIRECT_REPORT_NAME = ("Direct PO's - " + timestamp + ".png")
driver.save_screenshot(DIRECT_REPORT_NAME)

#Select Tool PO List
selectReport = Select(driver.find_element_by_name('reportNamesDropDown'))
selectReport.select_by_value('2')

#Set Report Length
selectReport = Select(driver.find_element_by_name('pageRec'))
selectReport.select_by_value('2')

#Generate Report
driver.find_element_by_name('returnVal').click()
time.sleep(5)
TOOL_REPORT_NAME = ("Tool PO's - " + timestamp + ".png")
driver.save_screenshot(TOOL_REPORT_NAME)

#Set Report
selectReport = Select(driver.find_element_by_name('reportNamesDropDown'))
selectReport.select_by_value('0')
#vlaue 0 = Indirect PO List
#value 1 = Direct PO List
#value 2 = Tool PO LIst
#value 3 = Legacy Direct PO List
#value 4 = Legacy Indirect PO List


#Set Report Length
selectReport = Select(driver.find_element_by_name('pageRec'))
selectReport.select_by_value('2')
#value 0 = 25
#value 1 = 50
#value 2 = All

#Generate Report
driver.find_element_by_name('returnVal').click()
time.sleep(5)
INDIRECT_REPORT_NAME = ("Indirect PO's - " + timestamp + ".png")
driver.save_screenshot(INDIRECT_REPORT_NAME)

report_file_list = [INDIRECT_REPORT_NAME, DIRECT_REPORT_NAME, TOOL_REPORT_NAME]

yagmail_send.yag_send("Auto Reports " + shorttime,"Attached are screenshots of auto systems", report_file_list)

driver.quit()












