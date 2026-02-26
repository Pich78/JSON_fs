import argparse
import sys
import json
from .core import execute, execute_file

def main():
    parser = argparse.ArgumentParser(description="JSON File System Library")
    parser.add_argument('input', nargs='?', help="Input JSON file path (optional, reads from stdin if omitted)")
    parser.add_argument('-o', '--output', help="Output JSON file path (optional, writes to stdout if omitted)")
    
    args = parser.parse_args()
    
    if args.input:
        if args.output:
            execute_file(args.input, args.output)
        else:
            with open(args.input, 'r', encoding='utf-8') as f:
                request_dict = json.load(f)
            result = execute(request_dict)
            json.dump(result, sys.stdout, indent=2)
            sys.stdout.write('\n')
    else:
        # Read from stdin
        in_data = sys.stdin.read()
        if not in_data.strip():
            parser.print_help()
            sys.exit(1)
            
        request_dict = json.loads(in_data)
        result = execute(request_dict)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
        else:
            json.dump(result, sys.stdout, indent=2)
            sys.stdout.write('\n')

if __name__ == '__main__':
    main()
