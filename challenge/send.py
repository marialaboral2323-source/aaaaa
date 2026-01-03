from scapy.all import *
import netifaces as ni

def get_internal_ip(interface='eth0'):
    ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return ip

def calculate_neighbor_ip(own_ip):
    ip_parts = own_ip.split('.')
    ip_parts[3] = str((int(ip_parts[3]) + 1) % 256) 
    return '.'.join(ip_parts)

own_ip = get_internal_ip('eth0') 
neighbor_ip = calculate_neighbor_ip(own_ip)

target_host = neighbor_ip
target_port = 179

flag = "DH{fakeflagfakeflagfakeflagfakeflagfakeflagfakeflag}"

ip = IP(dst=target_host)
tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
malformed_syn = ip/tcp/Raw(load=flag)

send(malformed_syn)
