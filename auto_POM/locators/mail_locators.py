from selenium.webdriver.common.by import By

class MailLocator:
    # Locators for Signature
    URL = "https://vndev.hanbiro.com/ngw/app/#/mail/list/all/"
    BUTTON_SETTING = (By.XPATH, "//*[starts-with(@id, 'mCSB') and contains(@id, 'container')]/div/ul/li/a[contains(@ng-click,'showSetting();') and contains(.,' Settings')]")
    BUTTON_SIGNATURE = (By.XPATH, "//*[starts-with(@id, 'mCSB') and contains(@id, 'container')]//a[contains(., ' Signature')]")
    BUTTON_SIGNATURE_ADD = (By.XPATH, "//*[@id='settingSignatureController']//button[contains(@data-ng-click, 'goWrite()') and contains(., 'Add')]")
    SIGNATURE_TYPE = (By.XPATH, "//*[@id='write-form']//input[contains(@data-ng-model, 'signatureType')]//following-sibling::span[contains(., 'Text')]")
    FRAME_TEXT = (By.CLASS_NAME, "tox-edit-area__iframe")
    SIGNATURE_INPUT = (By.XPATH, "//body[@id='tinymce']/p")
    SIGNATURE_SAVE = (By.XPATH, "//button[contains(@data-ng-click, 'saveSignature($event)') and contains(., 'Save')]")

    SIGNATURE_LIST_ITEMS = (By.XPATH, "//div[@id='settingSignatureController']/div[2]/ul/li")
    DELETE_SIGNATURE = (By.XPATH, "//div[@id='settingSignatureController']/div[2]/ul/li/label/span")
    DELETE_SIGNATURE_CONFIRM = (By.XPATH, "//*[@id='settingSignatureController']//button[contains(@data-ng-click, 'deleteSigSelected()') and contains(., 'Delete')]")

    # Locators for auto sort
    BUTTON_AUTO_SORT = (By.XPATH, "//*[starts-with(@id, 'mCSB') and contains(@id, 'container')]//a[contains(., ' Auto-Sort')]")