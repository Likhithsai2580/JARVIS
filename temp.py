import json
def get_extension_info():
    with open("extensions/config_all.json", 'r') as f:
        data = json.load(f)
    
    extensions_info = []
    for extension in data['extensions']:
        extension_info = {
            'name': extension['name'],
            'description': extension['description'],
            'parameters': extension['parameters']
        }
        extensions_info.append(extension_info)
    
    return extensions_info

print(get_extension_info())