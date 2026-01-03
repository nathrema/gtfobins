# gtfobins 

GTFOBins on the command line


## Install
```
wget https://raw.githubusercontent.com/nathrema/gtfobins/refs/heads/main/install.sh | sudo sh
```

## Uninstall
```
wget https://raw.githubusercontent.com/nathrema/gtfobins/refs/heads/main/uninstall.sh | sudo sh

```

## Help
```
usage: gtfobins [-h]
                [-f [{shell,command,reverse-shell,non-interactive-reverse-shell,bind-shell,non-interactive-bind-shell,file-upload,file-download,file-write,file-read,library-load,suid,sudo,capabilities,limited-suid,s,c,rs,nirs,bs,nibs,fu,fd,fw,fr,ll,si,su,a,lsi} ...]]
                [-l] [-s]
                [binary ...]

GTFOBins is a curated list of Unix binaries that can be used to bypass local security
restrictions in misconfigured systems.

positional arguments:
  binary                the binaries to search for

options:
  -h, --help            show this help message and exit
  -f, --function [{shell,command,reverse-shell,non-interactive-reverse-shell,bind-shell,non-interactive-bind-shell,file-upload,file-download,file-write,file-read,library-load,suid,sudo,capabilities,limited-suid,s,c,rs,nirs,bs,nibs,fu,fd,fw,fr,ll,si,su,a,lsi} ...]
                        filter results by function
  -l, --list            print only binary names
  -s, --stdin           read binary list from stdin
```
