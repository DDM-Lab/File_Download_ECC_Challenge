#!/usr/bin/env python3
import json
import os
import random
import tarfile
import re
import sys

flag = os.environ.get("FLAG")
if flag == "":
    print("Flag was not read from environment. Aborting.")
    sys.exit(-1)
else:
    flag_rand = re.search("{.*}$", flag)
if flag_rand == None:
    print("Flag isn't wrapped by curly braces. Aborting.")
    sys.exit(-2)
else:
    flag_rand = flag_rand.group()
    flag_rand = flag_rand[1:-1]

new_flag = "picoCTF{InC_Reused_Nonce_Vulnerability_" + flag_rand + "}"

metadata = {"flag": new_flag}

with open("/challenge/metadata.json", "w") as f:
    f.write(json.dumps(metadata))