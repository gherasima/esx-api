import subprocess
import argparse
import os
import json

# ---------------- Other Parameters -------------------------------------

esx_cli = '/usr/bin/esxcli '
vmware_cmd = '/usr/bin/vmware-cmd '

# ---------------- Program Begin -------------------------------------

parser = argparse.ArgumentParser(description='ESXi API')
parser.add_argument("-c", "--create_snapshot", help="", type=bool)
parser.add_argument("-r", "--revert_snapshot", help="", type=bool)
parser.add_argument("-n", "--snapshot_name", help="", type=str)
parser.add_argument("-s", "--start_vm", help="", type=bool)
parser.add_argument("-j", "--json_file", help="", type=str)
args = parser.parse_args()


def revert_to_last_snapshot(vm_list, datastore_path):
    for vm in vm_list:
        cmd = vmware_cmd + datastore_path + vm + '/' + vm + '.vmx revertsnapshot'
        cmd_run = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        std_out = cmd_run.stdout.decode()
        std_err = cmd_run.stderr.decode()
        print('std_out: ', std_out)
        print('std_out: ', std_err)
        print('return code: ', cmd_run.returncode)


def crete_snapshot(vm_list, datastore_path, snapshot_name):
    for vm in vm_list:
        cmd = vmware_cmd + datastore_path + vm + '/' + vm + '.vmx createsnapshot ' + snapshot_name + ' none 0 0'
        cmd_run = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        std_out = cmd_run.stdout.decode()
        std_err = cmd_run.stderr.decode()
        print('std_out: ', std_out)
        print('std_out: ', std_err)
        print('return code: ', cmd_run.returncode)


def start_vm(vm_list, datastore_path):
    for vm in vm_list:
        cmd = vmware_cmd + datastore_path + vm + '/' + vm + '.vmx start'
        cmd_run = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        std_out = cmd_run.stdout.decode()
        std_err = cmd_run.stderr.decode()
        print('std_out: ', std_out)
        print('std_out: ', std_err)
        print('return code: ', cmd_run.returncode)


if __name__ == '__main__':
    if args.json_file:
        # Open JSON file
        with open(args.json_file) as json_file:
            data_dict = json.load(json_file)
            # Set env parameters
            os.environ['VI_USERNAME'] = data_dict["VI_USERNAME"]
            os.environ['VI_PASSWORD'] = data_dict["VI_PASSWORD"]
            os.environ['VI_PROTOCOL'] = data_dict["VI_PROTOCOL"]
            os.environ['VI_SERVER'] = data_dict["VI_SERVER"]
            os.environ['VI_THUMBPRINT'] = data_dict["VI_THUMBPRINT"]
            # Set parameters
            datastore_path = data_dict["DATASTORE_PATH"]
            vm_list_master_first = data_dict["VM_LIST_MASTER_LAST"]
            vm_list_master_last = data_dict["VM_LIST_MASTER_LAST"]

            if args.create_snapshot:
                crete_snapshot(vm_list_master_last, datastore_path, args.snapshot_name)
            if args.revert_snapshot:
                revert_to_last_snapshot(vm_list_master_last, datastore_path)
            if args.start_vm:
                start_vm(vm_list_master_first, datastore_path)
