# Unicloud services
# for downloads, uploads and other background things

import os
argument = os.environ.get('PYTHON_SERVICE_ARGUMENT','')

import sys
sys.path.append('libs')

from plyer import notification 
from time import sleep
        

if __name__=='__main__':
    pass
    # while True:
    #     sleep(8)
    #     notification.notify(title='Service Started',message='Unicloud has started a service!!')
    #     print('servings: ',argument )
