## copied from http://www.caida.org/projects/ark/vela/web-api/
#!/usr/bin/env python

#############################################################################
## Convenience tool for exploring/testing the Vela web API.
##
#############################################################################

"""Usage:
  vela-api [options] mons
  vela-api [options] (trace | ping) <MON> <TARGET>
  vela-api [options] get <RESULT_ID>
  vela-api (-h | --help)
  vela-api --version

Options:
  --key STR     Vela API key.
  --url URL     Vela API base URL [default: https://vela.caida.org/api].
  --timeout NUM  HTTP request timeout (secs) [default: 120].
  --debug       Print additional debugging information.
  -h --help     Show this screen.
  --version     Show version.
"""

import os
import sys
import time

import requests

from docopt import docopt
args = docopt(__doc__, version='0.1')

g_api_key = args["--key"] or os.environ.get("VELA_API_KEY", None)
if not g_api_key:
   print >>sys.stderr, "ERROR: missing --key or $VELA_API_KEY"
   sys.exit(1)   

g_base_url = args["--url"]
g_debug = args["--debug"]

try:
   g_timeout = int(args["--timeout"])
   if g_timeout < 0: raise RuntimeError
except:
   print >>sys.stderr, \
      "ERROR: invalid --timeout argument; must be a number >= 0"
   sys.exit(1)


#===========================================================================
# MAIN
#===========================================================================

def print_mons(d, k):
   v = d[k]
   print ("{} {} = {}".format(len(v), k, ",".join(sorted(v))))
   print

def print_category_mons(d, k):
   print k + ":"
   for name,v in sorted(d[k].items()):
      print "   {} {} = {}".format(len(v), name, ",".join(v))
   print


#---------------------------------------------------------------------------

params = {'key': g_api_key}

if args["mons"]:
   r = requests.get(g_base_url + "/monitors", params=params, timeout=g_timeout)

elif args["trace"] or args["ping"]:
   params["destination"] = args["<TARGET>"]
   params["method"] = ("traceroute" if args["trace"] else "ping")
   params["vp"] = args["<MON>"]
   r = requests.post(g_base_url + "/create", params=params, timeout=g_timeout)

elif args["get"]:
   params["id"] = args["<RESULT_ID>"]
   r = requests.get(g_base_url + "/results", params=params, timeout=g_timeout)

print "URL: " + r.url
print "HTTP response code: " + str(r.status_code)
print "HTTP response body: " + r.text
print

result = r.json()

if result["result"] == "error":
   print "request error: " + result["message"]
   sys.exit(1)

if args["mons"]:
   print_mons(result, "ipv4")
   print_mons(result, "ipv6")
   for category in ["by_continent", "by_country", "by_orgtype"]:
      print_category_mons(result, category)

elif args["trace"] or args["ping"]:
   print "result ID: {}".format(result["result_id"])

elif args["get"]:
   print "request status: " + result["status"]

   start_date = time.ctime(result["start_timestamp"])
   print "measurement submission date: " + start_date

   if result["status"] == "completed":
      for k in ["values", "errors"]:
         print k + ":"
         for mon, v in result[k].iteritems():
            print "  {} = {}".format(mon, v)
            print

