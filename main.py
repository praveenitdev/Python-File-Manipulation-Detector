import os
import json
import hashlib
import optparse

def generateHash(file_path):
    with open(file_path,'r') as f:
        content = f.read()
        digest = hashlib.sha256(bytes(content,'utf-8')).hexdigest()
    return digest

def getFolderIntegrity(folder):
    data = {}
    data[folder]={}
    for file in os.listdir(folder):
        file_path = folder+"/"+file
        data[folder][file]= generateHash(file_path)
    return data
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--scan', help='provide the folder name to save integrity', type='str', dest='scan_folder_name')
    parser.add_option('--audit', help='provide the folder name to check integrity', type='str', dest='audit_folder_name')

    (options,args) = parser.parse_args()

    if options.scan_folder_name and options.scan_folder_name != None:
        with open('config.json','w') as config_file:
            config_file.write(json.dumps(getFolderIntegrity(options.scan_folder_name),indent=2))

    if options.audit_folder_name and options.audit_folder_name != None:
        with open('config.json','r') as config_file:
            config = json.loads(config_file.read())
        old_data = config[options.audit_folder_name]
        new_data = getFolderIntegrity(options.audit_folder_name)[options.audit_folder_name]
    
        for file_name, file_hash in old_data.items():
            if new_data[file_name] == file_hash:
                print(f'File integrity PASSED for file [{file_name}]')
            else:
                print(f'File integrity FAILED for file [{file_name}]')
                
        