from settings import *

DEBUG = False

IP = '154.117.8.18'
ALLOWED_HOSTS = [IP]

# Billing settings
BILLING_URL = "http://" + IP + ":8080/"
PACKAGES_URL = BILLING_URL + "packages/"
PACKAGE_INSERT_URL = PACKAGES_URL + "insert/"
PACKAGE_DELETE_URL = PACKAGES_URL + "delete/"
INSTANT_VOUCHER_INSERT_URL = PACKAGES_URL + "insert_vouchers/"

# Report recipients
VOUCHER_GEN_REPORT_TO = [
        'wakinje@spectrawireless.com', 
        'sdarko@spectrawireless.com',
        'georged@spectrawireless.com',
        'cbaah@spectrawireless.com',
        'cadzisu@spectrawireless.com',
        'fkabutey@spectrawireless.com',
        'ankitr@fb.com'
    ]