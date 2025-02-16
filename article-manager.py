#!/usr/bin python3

import os
import re
import hashlib
import json
import shutil

DRYRUN = os.getenv("DRY", "True").lower() in ("true", "1", "t")
OBVAULT_ARTICELS = os.getenv("OBVAULT_ARTICELS", "/mnt/c/Users/Rick/OneDrive/logseq documents/pages")
OBVAULT_ASSETS = os .getenv("OBVAULT_ASSETS", "/mnt/c/Users/Rick/OneDrive/logseq documents/assets")

# What script does:
# 1. scan each techblog article from vault
#   - properties
#       - title
#       - publish
#       - id
#   - images
#   - content hash
# 2. mark the article if publish is true
# 3. compare marked article hash with lockfile
#       in the lockfile:
#       - if id exist
#           - allow to publish, and content hash changed, update
#           - disallow to publish, delete
#       - if id does not exists 
#           - allow to publish, release the new article
#           - disallow to publish, disregard
# 4. copy article to .content
# 5. copy all images to static-{{properties.title}} folder under ./content if has any
# 6. next article
#
# Requirements:
# 1. script should be able to dry run
# 2. no 3th-party dependencies
# 3. should not change article during the process
# 4. non declared "publish" equals false
# 5. interrupting process should not cause state of lockfile loss


FILE_EXTENSION = ".md"
PROPERTY_DELIMITER = "---"
RELEVANT_PROPERTY_HANDLER = {
    "title": lambda s : s.strip(),
    "publish": lambda b : b.strip().lower() in ("true", "1", "t"),
    "id": lambda id : id.strip(),
}
# match any markdown image reference
REGEX = re.compile("^\!\[\[(.*\.(gif|jpe?g|tiff?|png|webp|bmp))\]\]$")
ATCMETAARR = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class Action:
    NEW = f"{bcolors.OKGREEN}+{bcolors.ENDC}"
    UPDATE = f"{bcolors.WARNING}~{bcolors.ENDC}"
    DELETE = f"{bcolors.FAIL}-{bcolors.ENDC}"

print(f"Scaning articles for publishing... \ndry run: {DRYRUN} in directory {OBVAULT_ARTICELS}\n")

# lockfile
lckfname = "./article-lock.json"
lck = {}
try:
    with open(lckfname, "r") as lckf:
        lck = json.load(lckf)
except FileNotFoundError as e:
    print("no article-lock.json file exists")

# process individual file
for fname in os.listdir(OBVAULT_ARTICELS):
    if not fname.strip().endswith(FILE_EXTENSION): 
        print(f"'{fname}' skipped: not a markdown file")
        continue

    with open(os.path.join(OBVAULT_ARTICELS, fname), "r") as f:
        print(f"process '{fname}'...")
        if not f.readline().strip().startswith(PROPERTY_DELIMITER):
            print("file skipped: doesn't follow property format")
            continue

        # retrieve properties
        meta = {"publish":False, "fname": fname}
        line = f.readline().strip()
        while not line.startswith(PROPERTY_DELIMITER):
            field = line.split(":", 1)
            key = field[0].strip()
            h = RELEVANT_PROPERTY_HANDLER.get(key, None)
            if h:
               val = field[1].strip()
               meta[key] = h(val)
            line = f.readline().strip()
        
        # retrieve images and content hash of the article
        if meta.get("publish") is True:
            # finds images of article and add to list
            while line := f.readline():            
                res = REGEX.search(line.strip())
                if res:
                    meta.setdefault("images", []).append(res.group(1))

            # obtains the hash of the article
            buf = bytearray(65536)
            sha1 = hashlib.sha1()
            f.buffer.seek(0) # back to the beginning of the file
            while f.buffer.readinto(buf) != 0:
                sha1.update(buf)
                buf.clear()
            meta.setdefault("hash", sha1.hexdigest())

        # decides action to article
        id = meta.get("id", None)
        hash = meta.get("hash", None)
        if meta["publish"] is True:
            if id not in lck:
                meta.setdefault("action", Action.NEW)
            elif lck.get(id).get("hash", None) != hash:
                meta.setdefault("action", Action.UPDATE)
        else:
            if id in lck:
                meta.setdefault("action", Action.DELETE)

        if "action" in meta:
            ATCMETAARR.append(meta) 

print("\n================================Dry Run Result================================\n")

print(f"Articles ready to publish: {Action.NEW}, remove: {Action.DELETE}, update: {Action.UPDATE}\n")
i = 1
for at in ATCMETAARR:
    print(f'{at["action"]} {i}. {at["title"]}:')
    print(f'id:{at["id"]}')
    print(f'hash:{at.get("hash")}')
    print(f'images:{at.get("images",{})}')
    print(f'\n')
    i+=1

if len(ATCMETAARR) == 0:
    print("nothing to update")

print("\n==============================================================================\n")

def apply():
    lckfnametemp = lckfname + ".tmp"
    if os.path.exists(lckfnametemp):
        raise Exception("temp lock file exists, manually conflict resolution needed")

    for meta in ATCMETAARR:
        targetfolder = "./content"
        staticfolder = f'{targetfolder}/static-{meta["fname"]}'
        fname = meta["fname"]
        match meta["action"]:
            case Action.NEW:
                if not os.path.exists(staticfolder):
                    print(meta)
                    if "images" in meta:
                        os.makedirs(staticfolder)
                        for img in meta["images"]:
                            shutil.copyfile(os.path.join(OBVAULT_ASSETS, img), os.path.join(staticfolder, img)) 
                    shutil.copyfile(os.path.join(OBVAULT_ARTICELS, fname), os.path.join(targetfolder, fname))
                    lck[meta["id"]] = meta
                else:
                    print(f'static folder for article {meta["fname"]} exists, manually conflict resolution needed')
                    return
            case Action.UPDATE:
                if os.path.exists(staticfolder):
                    shutil.rmtree(staticfolder)

                if "images" in meta:
                    os.makedirs(staticfolder)
                    for img in meta["images"]:
                        shutil.copyfile(os.path.join(OBVAULT_ASSETS, img), os.path.join(staticfolder, img)) 
                shutil.copyfile(os.path.join(OBVAULT_ARTICELS, fname), os.path.join(targetfolder, fname))
                lck[meta["id"]] = meta
            case Action.DELETE:
                if os.path.exists(staticfolder):
                    shutil.rmtree(staticfolder)
                os.remove(os.path.join(targetfolder, fname)) 
                lck.pop(meta["id"])

    with open(lckfnametemp, "w+") as lckft:
        json.dump(lck, lckft, indent=4)
    if os.path.exists(lckfname):
        os.remove(lckfname)
    os.rename(lckfnametemp, lckfname)

    print("done")


if not DRYRUN:
    if "yes" == input("type yes if you want to apply the change:\n\n"):
        apply()
    else:
        print("operation abort")
