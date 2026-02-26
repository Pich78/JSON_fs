import json_fs.core as core

def run():
    print("TEST 1: Valid List")
    print(core.execute({'action': 'list', 'path': '.'})['status'])
    
    print("\nTEST 2: Missing Path")
    print(core.execute({'action': 'list'})['status'])
    print(core.execute({'action': 'list'})['message'])
    
    print("\nTEST 3: Invalid Action")
    print(core.execute({'action': 'invalid_action'})['status'])
    print(core.execute({'action': 'invalid_action'})['message'])

if __name__ == '__main__':
    run()
