# -*- coding: utf-8 -*-
"""
The dict ``url`` defines a mapping from common names for phone's action to their action url.
It is case insensitive.

Now it only used in :class:MSGController
"""

url = {

    'dial': 'http://{usr}:{pwd}@{ip}/Phone_ActionURL&Command=1&Number={ext}&Account={line}'
}

# x = _url['dial'].format(usr='admin', pwd='admin', ip='10.3.3.191', ext='2055', line='1')
# print(x)

x = 'ok'
x.join('yes')
print(x.join('yes', 'no'))

