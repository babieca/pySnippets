#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nmap
import random
import netaddr
import csv
import datetime

def log2file(fpath, text):
    
    f = open(fpath,'a')
    f.write(text + '\n')
    f.flush()
    f.close()


def main():
    
    chunks = 10000
    wfile = './ssl443-IT.v0.certs'
    argsNmap = '-n -Pn -sS -p443 --script ssl-cert ' \
               '--host-timeout 1 --max-retries 1 ' \
               '--min-parallelism 1000'
    
    print('Starging...\nNmap:{}'.format(argsNmap))
    
    #Italy
    fname = './IP_range'
    rangeIPs = list(csv.reader(open(fname, 'r'), delimiter='\t'))
    random.shuffle(rangeIPs)

    req_total = 0
    req_valid = 0
    counter = 0
    iplst = []
    for r in rangeIPs:
        iprange = netaddr.IPRange(r[0], r[1])
        data = { "counter": counter,
                 "ip_range" : iprange,
                 "ip_size": iprange.size,
                 "ip_min" : r[0],
                 "ip_max" : r[1]}
        iplst.append(data)
        counter = counter + iprange.size

    if chunks > counter:
        chunks = counter
    
    irand = random.sample(range(0,counter), counter)
    
    j = 0
    t1 = datetime.datetime.now()
    t2_prev = t1
    while j < counter:
        
        ips = []
        
        for i in range(j,j+chunks):
            k = 0
            while (iplst[k]["counter"] + iplst[k]["ip_size"]) < irand[i]:
                k +=1
            
            ip_min = netaddr.IPAddress(iplst[k]["ip_min"])
            ip = ip_min + (irand[i] - iplst[k]["counter"])

            ips.append(ip.format())

        all_hosts = ' '.join(ips)
        nm = nmap.PortScanner()
        nm.scan(hosts=all_hosts, arguments=argsNmap)

        tags = ['tcp', 443, 'script', 'ssl-cert']
        for host in nm.all_hosts():
            item = nm[host]
            for tag in tags:
                if tag in item:
                    item = item[tag]
                    if tag==tags[-1]:
                        log2file(wfile, '{}|{}'.format(host, item.replace('\n','\\n')))
                        req_valid += 1
                else:
                    break
                
            req_total +=1
        t2 = datetime.datetime.now()
        print("{:{dfmt} {tfmt}}\tElapsed(Total): {}\tElapsed(Last): {}\tTotal requests: {}\tValid requests: {}".format(t2,
                                                                        t2-t1,
                                                                        t2-t2_prev,
                                                                        req_total, req_valid,
                                                                        dfmt='%Y-%m-%d',
                                                                        tfmt='%H:%M:%S'))
        t2_prev = t2
            
        j +=chunks


if __name__ == '__main__':
    main()
    
