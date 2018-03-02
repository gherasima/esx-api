import os

# ---------------- VCenter Parameters -------------------------------------

os.environ['VI_USERNAME'] = 'administrator@vc.local'
os.environ['VI_PASSWORD'] = 'password'
os.environ['VI_PROTOCOL'] = 'https'
os.environ['VI_SERVER'] = 'vcsa.vc.local'
os.environ['VI_THUMBPRINT'] = 'A5:B7:1A:0F:64:97:33:80:9A:DF:D9:6D:FE:38:4D:3F:E4:39:93:C1'


# ---------------- ESX Parameters -------------------------------------

esx_hosts = ['esx8']
