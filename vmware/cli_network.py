
import sys
import subprocess
from setting_vcenter import *
from setting_network import *


# ---------------- Program Begin -------------------------------------

esx_cli = 'esxcli -h '


def add_vswitch(hosts, names):
    for esx in hosts:
        for name in names:
            cmd = esx_cli + esx + ' network vswitch standard add --vswitch-name ' + name[0]
            cmd_run = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            std_out = cmd_run.stdout.decode()
            std_err = cmd_run.stderr.decode()
            print('Log: ', std_out)
            print('Error: ', std_err)


def add_portgroup(hosts, names):
    for esx in hosts:
        for name in names:
            cmd = esx_cli + esx + ' network vswitch standard  portgroup add --vswitch-name=' + name[0] + ' --portgroup-name=' + name[1]
            cmd_run = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            std_out = cmd_run.stdout.decode()
            std_err = cmd_run.stderr.decode()
            print('Log: ', std_out)
            print('Error: ', std_err)


def add_zan_portgroup(hosts, ports):
    for esx in hosts:
        for port in ports:
            cmd = esx_cli + esx + ' network vswitch standard  portgroup add --vswitch-name=' + port[0] + ' --portgroup-name=' + port[1]
            cmd_run = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            std_out = cmd_run.stdout.decode()
            std_err = cmd_run.stderr.decode()
            print('Log: ', std_out)
            print('Error: ', std_err)
            cmd = esx_cli + esx + ' network vswitch standard  portgroup set --portgroup-name=' + port[1] + ' --vlan-id=' + port[2]
            cmd_run = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            std_out = cmd_run.stdout.decode()
            std_err = cmd_run.stderr.decode()
            print('Log: ', std_out)
            print('Error: ', std_err)


def insert_zan_portgroup(hosts, zan_switch, port_group, vlan_id):
    for esx in hosts:
        cmd = esx_cli + esx + ' network vswitch standard  portgroup add --vswitch-name=' + zan_switch + ' --portgroup-name=' + port_group
        cmd_run = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        std_out = cmd_run.stdout.decode()
        std_err = cmd_run.stderr.decode()
        print('Log: ', std_out)
        print('Error: ', std_err)

        cmd = esx_cli + esx + ' network vswitch standard  portgroup set --portgroup-name=' + port_group + ' --vlan-id=' + vlan_id
        cmd_run = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        std_out = cmd_run.stdout.decode()
        std_err = cmd_run.stderr.decode()
        print('Log: ', std_out)
        print('Error: ', std_err)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Working...')
        #add_vswitch(esx_hosts, virtual_switch)
        #add_portgroup(esx_hosts, virtual_switch)
        #add_zan_portgroup(esx_hosts, zan_vswitch)
    else:
        portname = sys.argv[1]
        vlanid = sys.argv[2]
        insert_zan_portgroup(esx_hosts, zan_vswitch, portname, vlanid)


