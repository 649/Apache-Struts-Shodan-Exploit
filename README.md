# APACHE STRUTS SHODAN EXPLOIT POC

* Author: [@037](https://twitter.com/037)

Original code can be found [here](https://github.com/hook-s3c/CVE-2018-11776-Python-PoC).

This tool takes advantage of CVE-2018-11776 and Shodan to perform mass exploitation of verified and vulnerable Apache Struts servers.
Shodan search parameter has been left out to weed out any skids trying to use this tool for malicious reasons. This tool is created to be treated as a proof of concept for researchers not an attack tool.

It's important to also mention this tool verifies if the host is vulnerable before performing the exploit process. Making simulated attacks stealthy.

### Prerequisites

You're required to install Python 3.x

```
apt-get install python3
```

You are also required to have Shodan module installed

```
pip install shodan
```


### Using Shodan API

This tool requires you to own an upgraded Shodan API

You may obtain one for free in [Shodan](https://shodan.io/) if you sign up using a .edu email.

![alt text](https://raw.githubusercontent.com/649/Apache-Struts-Shodan-Exploit/master/1.png)