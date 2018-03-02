from conf.setting import *
import argparse
import sys

#############################################################################
# Arguments
#############################################################################

parser = argparse.ArgumentParser(description='VCenter API')
parser.add_argument("-r", "--revert_snapshoot", help="", action="store_true")
parser.add_argument("-c", "--create_snapshoot", help="", action="store_true")
parser.add_argument("-d", "--delete_snapshoot", help="", action="store_true")
parser.add_argument("-n", "--snapshoot_name", help="", type=str)
parser.add_argument("-s", "--start_vm", help="", action="store_true")
parser.add_argument("-p", "--stop_vm", help="", action="store_true")
parser.add_argument("-g", "--go", help="", action="store_true")
parser.add_argument("-f", "--vm_list_file", help="", type=str)
args = parser.parse_args()

#############################################################################
# Connect to ESX / VCenter
#############################################################################


def connect():
    from pyVim import connect
    esx_vcenter = connect.ConnectNoSSL(esx_vcenter_host, 443, esx_vcenter_user, esx_vcenter_pass)
    return esx_vcenter

#############################################################################
#   Functions
#############################################################################


def vm_name_to_object(vm_name, esx_obj):
    """ Receive a VM (text) name and return a vim.VirtualMachine object """
    datacenter = esx_obj.content.rootFolder.childEntity[0]
    vms = datacenter.vmFolder.childEntity
    for vm in vms:
        if vm.name == vm_name:
            return vm
    else:
        sys.exit('VM does not exist, program will not continue, aborting!!!')


def vm_have_snapshot(vm_object):
    """ return snapshot_root_object if the vm have snapshot(s)"""
    if vm_object:
        if vm_object.snapshot:
            return vm_object.snapshot.rootSnapshotList


def list_all_snapshots(snapshot_root_object):
    """receive vm_object.snapshot.rootSnapshotList """
    snapshot_list = []
    for snapshot in snapshot_root_object:
        snap_object = {'name': snapshot.name, 'object': snapshot.snapshot}
        snapshot_list.append(snap_object)
        try:
            snapshot_list = snapshot_list + list_all_snapshots(snapshot.childSnapshotList)
        except TypeError:
            return snapshot_list
        return snapshot_list


def revert_to_snapshot(vm_object, snapshot_name):
    # Check if vm has snapshot
    # If vm have snapshot return vm_object.snapshot.rootSnapshotList
    snapshot_root_object = vm_have_snapshot(vm_obj)

    # Create snapshot list
    if snapshot_root_object:
        snapshot_list = list_all_snapshots(snapshot_root_object)
    else:
        sys.exit('VM does not have any snapshot, program will not continue, aborting!!!')
    # Revert to specific snapshot
    if snapshot_root_object:
        # find snapshot object from list
        snapshot_success = False
        for snapshot in snapshot_list:
            if snapshot['name'] == snapshot_name:
                snapshot['object'].RevertToSnapshot_Task()
                print(vm_object.name, 'successfully revert to snapshot named', snapshot['name'])
                snapshot_success = True
        if not snapshot_success:
            sys.exit('VM snapshot named ' + snapshot['name'] + ' does not exist, program will not continue, aborting!!!')


def create_snapshot(vm_object, snapshot_name):
    name = snapshot_name
    description = ""
    dumpMemory = False
    quiesce = False
    vm_object.CreateSnapshot(name, description, dumpMemory, quiesce)


def revert_to_current_snapshot(vm_object):
    vm_object.RevertToCurrentSnapshot()


def delete_snapshoot(vm_object, snapshot_name):
    # Check if vm has snapshot
    # If vm have snapshot return vm_object.snapshot.rootSnapshotList
    snapshot_root_object = vm_have_snapshot(vm_obj)

    # Create snapshot list
    if snapshot_root_object:
        snapshot_list = list_all_snapshots(snapshot_root_object)
    else:
        sys.exit('VM does not have any snapshot, program will not continue, aborting!!!')
    # Revert to specific snapshot
    if snapshot_root_object:
        # find snapshot object from list
        snapshot_success = False
        for snapshot in snapshot_list:
            if snapshot['name'] == snapshot_name:
                snapshot['object'].RemoveSnapshot_Task(False)
                print(vm_object.name, 'successfully deleted snapshot named', snapshot['name'])
                snapshot_success = True
        if not snapshot_success:
            sys.exit('VM snapshot named ' + snapshot['name'] + ' does not exist, program will not continue, aborting!!!')


def power_off_vm(vm_object):
    vm_object.PowerOff()
    print(vm_object.name, 'success power off')


def power_on_vm(vm_object):
    vm_object.PowerOn()
    print(vm_object.name, 'success power on')

#############################################################################
# Run program
#############################################################################


if __name__ == '__main__' and args.go:
    # Import specific vms.py file with vm_list tuple
    if args.vm_list_file:
        exec('from conf.' + args.vm_list_file + ' import vm_list')
        esx_object = connect()
        for name in vm_list:
            # Convert vm name to vm object
            vm_obj = vm_name_to_object(name, esx_object)

            if args.revert_snapshoot and args.snapshoot_name:
                revert_to_snapshot(vm_obj, args.snapshoot_name)

            if args.revert_snapshoot:
                revert_to_current_snapshot(vm_obj)

            if args.delete_snapshoot and args.snapshoot_name:
                delete_snapshoot(vm_obj, args.snapshoot_name)

            if args.create_snapshoot and args.snapshoot_name:
                create_snapshot(vm_obj, args.snapshoot_name)

            if args.start_vm:
                power_on_vm(vm_obj)

            if args.stop_vm:
                power_off_vm(vm_obj)
