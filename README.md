IPs  
 - 192.168.195.20  
 - 192.168.195.30  
 - 192.168.195.40

python -m venv /path/to/new/virtual/environment  
source <venv>/bin/activate

Pamiętać aby zmienić stałe IP oraz INITIAL_TRUSTED_IP

(venv) maciej@si:~/ffcoin $ sudo iptables -A INPUT -s 192.168.195.0/24 -p tcp -m tcp --dport 1939 -j ACCEPT  
(venv) maciej@si:~/ffcoin $ sudo iptables -A OUTPUT -s 192.168.195.0/24 -p tcp --sport 1939 -m state --state ESTABLISHED -j ACCEPT

