someStr = "'does it matter?'"
otherStr = ("can I say "+someStr+" in "
            "the middle?")
print(otherStr+" Yes.")
yetAnother = ("what about this? "
              +someStr+" or not work?")
print(yetAnother+" IT WORKS!")


import os
import subprocess
pDir = 'cd'
subprocess.run([pDir], capture_output=True)
os.system(pDir)
os.system('ls')

print(subprocess.getoutput)
# not working
