from settings import *

IP = '154.117.8.19'
ALLOWED_HOSTS = [IP]

# Billing settings
BILLING_URL = "http://" + IP + ":7700/"
PACKAGES_URL = BILLING_URL + "packages/"
PACKAGE_INSERT_URL = PACKAGES_URL + "insert/"
PACKAGE_DELETE_URL = PACKAGES_URL + "delete/"
INSTANT_VOUCHER_INSERT_URL = PACKAGES_URL + "insert_vouchers/"

# Report recipients
VOUCHER_GEN_REPORT_TO = ['alwaysdeone@gmail.com']