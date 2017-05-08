from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vms_test',
        'USER': 'vms',
        'PASSWORD': 'vmspass',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

# Billing settings
BILLING_URL = 'http://154.117.8.19/'

# Report recipients
VOUCHER_GEN_REPORT_TO = ['alwaysdeone@gmail.com']