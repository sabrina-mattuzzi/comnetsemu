
# Create the configuration and log files
touch /etc/quagga/zebra.conf
touch /etc/quagga/ripd.conf
touch /etc/quagga/ospfd.conf
touch /etc/quagga/vtysh.conf



touch /var/log/zebra.log
touch /var/log/ripd.log
touch /var/log/ospfd.log

##ZEBRA
#conf
echo 'password zebra' >> /etc/quagga/zebra.conf
echo 'enable password zebra' >> /etc/quagga/zebra.conf
echo 'service advanced-vty' >> /etc/quagga/zebra.conf
echo 'log file /var/log/zebra.log' >> /etc/quagga/zebra.conf
echo 'line vty' >> /etc/quagga/zebra.conf
#log
echo 'cat /etc/quagga/zebra.conf' >> /var/log/zebra.log
echo 'log syslog' >> /var/log/zebra.log
echo 'log facility local7' >> /var/log/zebra.log
echo 'log file /var/log/zebra.log' >> /var/log/zebra.log

##RIPD
#conf
echo 'password zebra' >> /etc/quagga/ripd.conf
echo 'enable password zebra' >> /etc/quagga/ripd.conf
echo 'router rip' >> /etc/quagga/ripd.conf
echo 'redistribute connected' >> /etc/quagga/ripd.conf
echo 'network eth1' >> /etc/quagga/ripd.conf
echo 'network eth2' >> /etc/quagga/ripd.conf
echo 'network eth3' >> /etc/quagga/ripd.conf
echo 'service advanced-vty' >> /etc/quagga/ripd.conf
echo 'log file /var/log/ripd.log' >> /etc/quagga/ripd.conf
echo 'line vty' >> /etc/quagga/ripd.conf
#log
echo 'cat /etc/quagga/ripd.conf' >> /var/log/ripd.log
echo 'log syslog' >> /var/log/ripd.log
echo 'log facility local7' >> /var/log/ripd.log
echo 'log file /var/log/ripd.log' >> /var/log/ripd.log

##OSPFD
#conf
echo 'password zebra' >> /etc/quagga/ospfd.conf
echo 'enable password zebra' >> /etc/quagga/ospfd.conf
echo 'interface eth1' >> /etc/quagga/ospfd.conf
echo 'ospf cost 30' >> /etc/quagga/ospfd.conf
echo 'router ospf' >> /etc/quagga/ospfd.conf
echo 'no ospf router-id' >> /etc/quagga/ospfd.conf
echo 'network 10.0.0.0/16 area 0.0.0.0' >> /etc/quagga/ospfd.conf
echo 'redistribute connected' >> /etc/quagga/ospfd.conf
echo 'service advanced-vty' >> /etc/quagga/ospfd.conf
echo 'log file /var/log/ospfd.log' >> /etc/quagga/ospfd.conf
echo 'line vty' >> /etc/quagga/ospfd.conf
#log
echo 'cat /etc/quagga/ripd.conf' >> /var/log/ospfd.log
echo 'log syslog' >> /var/log/ospfd.log
echo 'log facility local7' >> /var/log/ospfd.log
echo 'log file /var/log/ospfd.log' >> /var/log/ospfd.log

# Change the owner and the mode of the files
chown quagga:quagga /etc/quagga/zebra.conf && chmod 640 /etc/quagga/zebra.conf
chown quagga:quagga /etc/quagga/ripd.conf && chmod 640 /etc/quagga/ripd.conf
chown quagga:quagga /etc/quagga/ospfd.conf && chmod 640 /etc/quagga/ospfd.conf

chown quagga:quaggavty /var/log/zebra.log
chown quagga:quaggavty /var/log/ripd.log
chown quagga:quaggavty /var/log/ospfd.log
chown quagga:quaggavty /etc/quagga/vtysh.conf

echo 'username root nopassword' >>  /etc/quagga/vtysh.conf
echo "export VTYSH_PAGER=more" >>  /etc/bash.bashrc
echo 'VTYSH_PAGER=more' >>  /etc/environment

# Edit telnet access and the retaining of routes over restarts
echo 'vtysh_enable=yes' >> /etc/quagga/debian.conf
echo 'zebra_options=" --daemon -A 127.0.0.1 -P 2601 -u quagga --keep_kernel --retain"' >> /etc/quagga/debian.conf
echo 'ripd_options=" --daemon -A 127.0.0.1 -P 2602 -u quagga --retain"' >> /etc/quagga/debian.conf
echo 'ospfd_options=" --daemon -A 127.0.0.1 -P 2604 -u quagga"' >> /etc/quagga/debian.conf
