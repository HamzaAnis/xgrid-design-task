## Design Task

[![N|Solid](https://www.xgrid.co/wp-content/uploads/2018/02/logo.png)](https://www.xgrid.co/)
## Repository overview
```
│   .gitignore                  Files to be ignored by git.
│   blacklist_ip_list.json      To store the IP's that are blaclisted.
│   count_ip.json               To store the count of packets for blocked IP.
│   LICENSE                     GPL-3.0.
│   logging.conf                Configuration file for logging.
│   tunneling.sh                To configure the router tables on the simulator machine so they can ping each other for this design.
│
├───.vscode
│       settings.json           The configuration for the workspace.
│
└───xgrid                       Package main.
    │   __init__.py             Main file/ Starting point.
    │
    ├───database                Package database.
    │       __init__.py
    │
    ├───director                Package director.
    │       __init__.py
    │
    └───publisher               Package publisher.
            __init__.py
```
Dependenices:
  - [Pycore][l1]
  - [RPyc][l2]
  - [Scapy][l3]
  - [Python][l4]

**I highly recommend you to use Ubuntu 14.04 LTS.**

Setup all the dependencies

Clone & Configure

```sh
$ git clone https://github.com/HamzaAnis/xgrid-design-task.git
$ cd xgrid-design-task
$ bash tunelling.sh {remote-ip} {local-ip}
```
Run
```sh
$ python xgrid/__init__.py
```

License
----

GPL-3.0



   [l1]: <https://downloads.pf.itd.nrl.navy.mil/docs/core/core-html/scripting.html>
   [l2]: <https://rpyc.readthedocs.io/en/latest/)>
   [l3]: <https://scapy.net/>
   [l4]: <https://www.python.org/>
