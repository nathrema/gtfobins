#!/bin/python

import os,sys,argparse
from yaml import load_all, load, dump
from termcolor import colored
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

GTFO_PATH = os.path.dirname(os.path.realpath(__file__)) + '/GTFOBins.github.io'

def init(function_names):
    parser = argparse.ArgumentParser(prog='gtfobins',description='GTFOBins is a curated list of Unix binaries that can be used to bypass local security restrictions in misconfigured systems.')
    parser.add_argument('binary',nargs='*',help='the binaries to search for')
    parser.add_argument('-f','--function',choices=function_names,nargs='*',help='filter results by function',action='append')
    parser.add_argument('-l','--list',help='print only binary names',default=False,action='store_true')
    parser.add_argument('-s','--stdin',help='read binary list from stdin',default=False,action='store_true')
    parser.add_argument('-u','--update',help='update from GTFOBins',default=False,action='store_true')
    args = parser.parse_args()

    are_args_empty = (args.binary is None or len(args.binary) == 0) and args.function is None and not args.stdin
    if are_args_empty and not args.update:
        parser.print_help()
        exit()

    function = None
    if args.function is not None:
        function = list(map(lambda x: x[0], args.function))

    return [are_args_empty, args.binary, function, args.list, args.stdin, args.update]

def fetch_repo():
    if os.path.exists(GTFO_PATH):
        os.system(f'cd {GTFO_PATH} && git pull 2>/dev/null')
    else:
        os.system('git clone https://github.com/GTFOBins/GTFOBins.github.io 2>/dev/null')

def get_files(path,include=None):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        if include is None:
            f.extend(filenames)
        else:
            for filename in filenames:
                if include in filename:
                    f.append(filename)
        break
    return f

def translate_long_function(fn):
    match fn:
        case 's':
            return 'shell'
        case 'c':
            return 'command'
        case 'rs':
            return 'reverse-shell'
        case 'nirs':
            return 'non-interactive-reverse-shell'
        case 'bs':
            return 'bind-shell'
        case 'nibs':
            return 'non-interactive-bind-shell'
        case 'fu':
            return 'file-upload'
        case 'fd':
            return 'file-download'
        case 'fw':
            return 'file-write'
        case 'fr':
            return 'file-read'
        case 'll':
            return 'library-load'
        case 'si':
            return 'suid'
        case 'su':
            return 'sudo'
        case 'a':
            return 'capabilities'
        case 'lsi':
            return 'limited-suid'
    return fn 

def translate_short_function(fn):
    match fn:
        case 'shell':
            return 's'
        case 'command':
            return 'c'
        case 'reverse-shell':
            return 'rs'
        case 'non-interactive-reverse-shell':
            return 'nirs'
        case 'bind-shell':
            return 'bs'
        case 'non-interactive-bind-shell':
            return 'nibs'
        case 'file-upload':
            return 'fu'
        case 'file-download':
            return 'fd'
        case 'file-write':
            return 'fw'
        case 'file-read':
            return 'fr'
        case 'library-load':
            return 'll'
        case 'suid':
            return 'si'
        case 'sudo':
            return 'su'
        case 'capabilities':
            return 'a'
        case 'limited-suid':
            return 'lsi'
    return fn

def get_short_functions(function_names):
    short_functions=[]
    for name in function_names:
        short_functions.append(get_short_function(name))
    return short_functions

def load_functions():
    functions=None
    with open(f'{GTFO_PATH}/_data/functions.yml') as f:
        functions = load(f, Loader=Loader)
    return functions

def load_binaries():
    binaries={}
    for filename in get_files(f'{GTFO_PATH}/_gtfobins','.md'):
        with open(f'{GTFO_PATH}/_gtfobins/{filename}') as f:
            data={}
            name,ext = os.path.splitext(filename)
            for row in load_all(f, Loader=Loader):
                if row is None:
                    continue

                for key,value in row.items():
                    data[key]=value
            binaries[name] = data
    return binaries

def print_binary_header(name,row,list_only):
    description = None if not 'description' in row else row['description']
    if list_only:
        print(name)
    else:
        print(colored(name, attrs=['bold','reverse']))
        if description is not None:
            print(description)
        print()

def print_separator(char = '-'):
    width = os.get_terminal_size().columns
    print(char * width)

def print_function(name,functions):
    if name is not None:
        print(colored(f'{name}', attrs=['bold']))
    has_multiple = len(functions) > 1

    for i,item in enumerate(functions):
        is_last = i == len(functions) - 1

        if has_multiple:
            print(f'method #{i + 1}')
        for entry,text in item.items():
            print(f'{text}')

def binary_has_function(row,function):
    if 'functions' in row:
        return function in row['functions'].keys()
    return False

def binary_has_functions(row,functions):
    if 'functions' in row:
        for function in functions:
            if function in row['functions'].keys():
                return True
    return False

def print_functions(name,row,filter):
    if 'functions' in row:
        for function,list in row['functions'].items():
            if filter is not None and not function in filter:
                continue
            print_function(function,list)

functions = load_functions()
function_names = list(functions.keys()) + list(map(lambda x: translate_short_function(x), functions.keys()))
[are_args_empty,binary_filter,function_filter,list_only,from_stdin,should_update] = init(function_names)
binaries = load_binaries()
binary_names = binaries.keys()
was_function_filter_specified = function_filter is not None

if should_update or not os.path.exists(GTFO_PATH):
    print('updating...')
    fetch_repo()
    print('done\n')

if are_args_empty:
    exit()

if from_stdin:
    for line in sys.stdin.readlines():
        binary_filter.append(line)
used_binaries = binary_names if len(binary_filter) == 0 else binary_filter

if was_function_filter_specified:
    function_filter = list(map(lambda x: translate_long_function(x), function_filter))

filtered_binaries = []
for i,original_binary in enumerate(used_binaries):
    binary = os.path.basename(original_binary).strip()

    if not binary in binaries:
        continue

    if was_function_filter_specified and not binary_has_functions(binaries[binary], function_filter):
        continue

    if binary in filtered_binaries:
        continue

    filtered_binaries.append(binary)

if len(filtered_binaries) == 0:
    print("no entries")
    exit()

for i,binary in enumerate(filtered_binaries):
    should_print_separator = not list_only and i < len(filtered_binaries) - 1

    print_binary_header(binary, binaries[binary], list_only)
    if not list_only:
        print_functions(binary, binaries[binary], function_filter)

    if should_print_separator:
        print_separator()
