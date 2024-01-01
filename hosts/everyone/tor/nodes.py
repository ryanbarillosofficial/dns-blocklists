"""
Reference(s):
https://ihateregex.io/expr/ipv6/
"""
import requests as req
import re
import os
import textwrap
import datetime

nl = str("\n")
comment = textwrap.dedent("""\
# Title:
# Tor IP Addresses - All Nodes (TXT File)
#
# Description:
# Converts SecOps-Institute's Tor IP Address ".lst" to ".txt" for use
# in other DNS services like AdAway on Android. This fetches the latest
# original "lst" file and route the address to either "0.0.0.0" or "::0"
#
# Source(s) Used:
# https://github.com/SecOps-Institute/Tor-IP-Addresses
#
# Project Home Page:
# https://github.com/ryanbarillos/dns-blocklists
#
""")


# Test
def main():
    # RegEx
    ipv4Regex = re.compile("^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$")
    ipv6Regex = re.compile("(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))")

    # Lists
    ipv4 = []
    ipv6 = []

    #Strings
    fileName = str("nodes")
    div = str("#=========\n")

    # Get list of IP addresses of well-known Tor nodes
    url = "https://raw.githubusercontent.com/SecOps-Institute/Tor-IP-Addresses/master/tor-nodes.lst"
    res = req.get(url)
    
    # Convert response to list
    nodes = res.text.split("\n")
    
    # Move IP addresses to respective list
    for node in nodes:
        if ipv4Regex.match(node): ipv4.append("0.0.0.0 " + node)  
        elif ipv6Regex.match(node): ipv6.append("::0 " + node)  
    
    """
    Push results to .txt file:
        - Delete existing txt file 
        - Create new text file
        - Loop through all lists to push addresses to new txt file
    """
    if os.path.exists(fileName + ".txt"): os.remove(fileName + ".txt")
    file = open(fileName + ".txt", "x")
    file.write(comment)
    file.write("# Last Updated: " + datetime.date.today().strftime("%d %b %Y") + nl) 
    file.write("\n\n" + div + "IPv4 Nodes\n" + div)
    for i in ipv4:
        file.write(i + nl)
    file.write("\n\n" + div + "IPv6 Nodes\n" + div)
    for i in ipv6:
        file.write(i + nl)

# Run script    
main()