# OSINT port scanner 
## Features:
        +Zero request from your machine to target
        +Possible to use as much thread as number of IP addresses
        +Threads splits IP addresses between them and scans at the same time
        +Can scan port ranges and single port

## Usage:
        For single port:        python3 portscan.py <IP Subnet> <Thread Number> <Port>
        For multiple ports:     python3 portscan.py <IP Subnet> <Thread Number> <Starting Port> <End Port>
