import os

host_list = input("Enter the full path of the host file: ")

if os.path.exists(host_file):
  with open(f"{host_list}) as host_list:
            for host in host_list:
            os.system(f"enum4linux {host})
else:
  print("The path or file you entered does not exist...")
