
import subprocess
from setting_vcenter import *
from setting_datastore import *


# ---------------- Program Begin -------------------------------------

esx_cli = 'esxcli -h '


def add_nfs_datastore(hosts, names):
    for esx in hosts:
        for name in names:
            cmd = esx_cli + esx + ' storage nfs add --host=' + name[1] + ' --share=' + name[2] + ' --volume-name=' + name[0]
            cmd_run = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            std_out = cmd_run.stdout.decode()
            std_err = cmd_run.stderr.decode()
            print('Log: ', std_out)
            print('Error: ', std_err)


if __name__ == '__main__':
    print('Working...')
    add_nfs_datastore(esx_hosts, datastores)
