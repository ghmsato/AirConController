from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
import time


def myclick(d, x):
    """click on the item, but click will be intercepted by other handler
    Args:
        d (webdriver): driver
        x (text): XPATH
    """
    try:
        d.find_element(By.XPATH, x).click()
    except (exceptions.ElementClickInterceptedException, exceptions.ElementNotInteractableException):
        pass
    return


def mylogon(d):
    """open page and logon
    Args:
        d (webdriver): driver
    """
    # Open the page
    d.get('http://takeshiba-airweb.fortiddns.com/TenantServer/Account/Logon')

    # Wait until the page has been loaded
    element = WebDriverWait(d, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='TenantId']"))
    )

    # Input Login Information
    d.find_element(By.XPATH, "//*[@id='TenantId']").send_keys("Tokyoportcity0002")
    d.find_element(By.XPATH, "//*[@id='UserId']").send_keys("Tokyoportcity0002")
    d.find_element(By.XPATH, "//*[@id='Password']").send_keys("Takeshiba0002")
    d.find_element(By.XPATH, "//*[@id='btn-logon']").click()
    return


def mylogout(d):
    """logout
    Args:
        d (webdriver): driver
    """
    # Open logout page
    d.get('http://takeshiba-airweb.fortiddns.com/TenantServer/Account/Logout')
    
    # Wait until initial logon page has been loaded
    element = WebDriverWait(d, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='TenantId']"))
    )
    return


def selectfloor(d):
    """select floor and area
    Args:
        d (webdriver): driver
    """
    # Wait until the page has been loaded
    element = WebDriverWait(d, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='Condition_FloorId']"))
    )

    # select floor and area
    select_element = d.find_element(By.XPATH, "//*[@id='Condition_FloorId']")
    select = Select(select_element)
    select.select_by_visible_text('36F')
    select_element = d.find_element(By.XPATH, "//*[@id='Condition_AreaId']")
    select = Select(select_element)
    select.select_by_visible_text('C南')
    return


def airconon(d):
    """set Air Conditioner ON
    Args:
        d (webdriver): driver
    """
    # select ON/OFF
    myclick(d, "//*[@id='tenantServer']/div[2]/div[2]/div[1]/ul/li[1]")
    
    # Wait until the page has been loaded
    element = WebDriverWait(d, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='tenantServer']/div[2]/div[2]/div[2]/div[3]/ul/li[7]/div[5]"))
    )
    
    # if the current mode is OFF, click the room to select
    f = 0
    if d.find_element(By.XPATH, "//*[@id='tenantServer']/div[2]/div[2]/div[2]/div[3]/ul/li[7]/div[5]").text == "OFF":
        f = 1
        myclick(d, "//*[@id='tenantServer']/div[2]/div[2]/div[2]/div[3]/ul/li[7]")

    if d.find_element(By.XPATH, "//*[@id='tenantServer']/div[2]/div[2]/div[2]/div[3]/ul/li[10]/div[5]").text == "OFF":
        f = 1
        myclick(d, "//*[@id='tenantServer']/div[2]/div[2]/div[2]/div[3]/ul/li[10]")

    # if room has been selected, click Next, then execute ON
    if f == 1:
        # click Next
        myclick(d, "//*[@id='tenantServer']/div[2]/div[2]/div[2]/div[5]/a")
        # wait loading popup window
        element = WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div"))
        )
        # click ON
        myclick(d, "//*[@id='onoffSubmit']/div/div/div")
        time.sleep(1) # workaround
        # click Execute
        d.find_element(By.XPATH, "/html/body/div[7]/div/div[2]/button").click()
    return


def temp0(d):
    """set temperature +-0
    Args:
        d (webdriver): driver
    """
    # select temperature
    myclick(d, "//*[@id='tenantServer']/div[2]/div[2]/div[1]/ul/li[2]")
    
    # Wait until the page has been loaded
    element = WebDriverWait(d, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='tenantServer']/div[2]/div[2]/div[3]/div[3]/ul/li[7]/div[6]"))
    )

    # if the current temperature is not 0, click the room to select
    f = 0
    if d.find_element(By.XPATH, "//*[@id='tenantServer']/div[2]/div[2]/div[3]/div[3]/ul/li[7]/div[6]").text != "±0.0℃":
        f = 1
        myclick(d, "//*[@id='tenantServer']/div[2]/div[2]/div[3]/div[3]/ul/li[7]")

    if d.find_element(By.XPATH, "//*[@id='tenantServer']/div[2]/div[2]/div[3]/div[3]/ul/li[10]/div[6]").text != "±0.0℃":
        f = 1
        myclick(d, "//*[@id='tenantServer']/div[2]/div[2]/div[3]/div[3]/ul/li[10]")

    # if room has been selected, click Next, then set the temperature to 0
    if f == 1:
        # click Next
        myclick(d, "//*[@id='tenantServer']/div[2]/div[2]/div[3]/div[5]/a/div")
        # wait loading popup window
        element = WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div"))
        )
        # click the center of sliding bar
        myclick(d, "//*[@id='slider']")
        # click Execute
        myclick(d, "/html/body/div[8]/div/div[2]/button")
    return


def main():
    """main
    """
    options = webdriver.ChromeOptions()
    options.accept_insecure_certs = True
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # logon to the system
    mylogon(driver)

    # set Air Conditioner ON
    selectfloor(driver)
    airconon(driver)

    # set temperature to +-0
    selectfloor(driver)
    temp0(driver)

    # logout from the system
    mylogout(driver)

    driver.quit()
    return


if __name__ == '__main__':
    main()