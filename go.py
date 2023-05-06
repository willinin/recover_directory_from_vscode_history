import os
import json
import shutil

'''
after exec python go.py, vscode about "IFBC" directory will recover.
'''

# CONFIG，need to revise for using
VSCODE_HISTORY_PATH = "C:\\Users\\31579\\AppData\\Roaming\\Code\\User\\History"
RECOVER_DIR = "C:\\Users\\31579\\Desktop\\recover_test"

def cp(src_path, dst_path):
    shutil.copy(src_path, dst_path)

def recover(keyword):
    #for save recently timestamp for every file
    timestamp_dict = {}

    for root, dirs, files in os.walk(VSCODE_HISTORY_PATH):
        for dir_name in dirs:
            entry_file = VSCODE_HISTORY_PATH +"\\"+ dir_name + "\\entries.json"
            with open(entry_file, "r") as f:
                data = json.load(f)
            
            file_path = data['resource']
            if keyword in file_path:
                relative_path = file_path.split(keyword)[-1]
                relative_dir = os.path.dirname(relative_path)

                recover_dir  = RECOVER_DIR + "\\" + relative_dir
                if not os.path.exists(recover_dir):
                    os.makedirs(recover_dir)
                
                recover_path = RECOVER_DIR + "\\" + relative_path

                entry_list = data["entries"]

                src_path = VSCODE_HISTORY_PATH + "\\" + dir_name + "\\" + entry_list[-1]["id"]
                lastest_timestamp = entry_list[-1]['timestamp']
                #print(f"file:{src_path}, timestamp:{entry_list[-1]['timestamp']}")

                if os.path.exists(recover_path):
                    if lastest_timestamp > timestamp_dict[relative_path]:
                        cp(src_path, recover_path)
                else:
                    cp(src_path, recover_path)
                    timestamp_dict[relative_path] = lastest_timestamp

if __name__ == "__main__":
    print("[+] Start.")
    recover("IFBC/")
    print("[+] End.")
    