import argparse
import os
import shutil
import sys

# Paths for templates and copies
TEMPLATE_PATH = r'C:/tempM122/vmware/vmTemplates/'
COPY_PATH = r'C:/tempM122/vmware/vmCopies/'


def main():
    """
    Main function
    """
    vmname, users = parse_arguments()
    check_folders(vmname)
    vm_copy(vmname, users)


def parse_arguments():
    """
    Parse the arguments

    :return: the vmname and a list of users
    """
    parser = argparse.ArgumentParser(description='VM Copier Tool')
    parser.add_argument('vmname', type=str, help='Name of the VM to copy')
    parser.add_argument('users', nargs='+', type=str, help='List of users to create copies for')
    args = parser.parse_args()

    return args.vmname, args.users


def check_folders(vmname):
    """
    Check if the folders exist
    :param vmname: the name of the vm to copy
    """
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Template path does not exist: {TEMPLATE_PATH}")
        sys.exit(1)

    if not os.path.exists(os.path.join(TEMPLATE_PATH, vmname)):
        print(f"VM template '{vmname}' does not exist in the template path.")
        sys.exit(1)

    if not os.path.exists(COPY_PATH):
        print(f"Copy path does not exist. Creating: {COPY_PATH}")
        os.makedirs(COPY_PATH)


def vm_copy(vmname, users):
    """
    Copy the vm to the users
    :param vmname: the name of the vm to copy
    :param users: a list of users to create copies for
    """
    for user in users:
        create_copies(vmname, user)


def create_copies(vmname, user):
    """
    Copy the files from the template to the user folder, changing the name of the files
    :param vmname: the name of the vm to copy
    :param user: the user to create the copy for
    """
    user_path = os.path.join(COPY_PATH, user)
    vm_template_path = os.path.join(TEMPLATE_PATH, vmname)

    if not os.path.exists(user_path):
        print(f"Creating user folder: {user_path}")
        os.makedirs(user_path)

    print(f"Copying VM '{vmname}' to user folder '{user}'...")
    for item in os.listdir(vm_template_path):
        s = os.path.join(vm_template_path, item)
        d = os.path.join(user_path, f"{vmname}{user}{item}")
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    update_config(vmname, user)


def update_config(vmname, user):
    """
    Update the configuration files
    :param vmname: the name of the vm to copy
    :param user: the user to create the copy for
    """
    user_path = os.path.join(COPY_PATH, user)
    config_file_path = os.path.join(user_path, f"{vmname}_{user}_config.txt")  # Example config file
    print(f"Updating configuration file for user '{user}'...")

    # Example: Add custom configuration logic here
    with open(config_file_path, 'w') as config_file:
        config_file.write(f"VM Name: {vmname}\n")
        config_file.write(f"User: {user}\n")
        config_file.write("Configuration updated.\n")

    print(f"Configuration updated for user '{user}'.")


if _name_ == '_main_':
    main()
