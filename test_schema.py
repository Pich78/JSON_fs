import json
from json_fs.core import execute

if __name__ == "__main__":
    print("LEVEL 1: Summary List of Tools")
    print("-" * 40)
    level_1_req = {"action": "schema"}
    level_1_res = execute(level_1_req)
    print(json.dumps(level_1_res, indent=2))
    
    print("\n\n" + "=" * 40 + "\n\n")
    
    print("LEVEL 2: Detailed Schema for specific tool ('read')")
    print("-" * 40)
    level_2_req = {"action": "schema", "tool": "read"}
    level_2_res = execute(level_2_req)
    print(json.dumps(level_2_res, indent=2))
