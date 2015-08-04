#!/usr/bin/python

import argparse
import wget
import subprocess
import os.path
import zipfile
import urllib2
from datetime import date

# Import zlib for compression
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

# Define arguments for the parser
parser = argparse.ArgumentParser(description='History processor for Openstreetmap')
parser.add_argument('date', metavar='date', type=str, help='Date you want to start')
parser.add_argument('days', metavar='days', type=int, help='How many days history?')

args = parser.parse_args()
start_date = date(2012, 9, 12)
end_date = date(int(args.date.split('-')[0]), int(args.date.split('-')[1]), int(args.date.split('-')[2]))
delta = (end_date - start_date).days
days = args.days or 7;

# Utility function to run shell commands
def bash(command):
    "Runs a command in shell"
    subprocess.call(command, shell=True)
    return

# OSM repication server url and data team users
osm_replication_url = "http://planet.osm.org/replication/day/"

# Read from users.list
users = open('users.list', 'r').readlines()

if __name__ == "__main__":

    # Create a dir for the files
    bash("mkdir files")
    bash("cd files")
    while days>=0:

        # Set the current edition number
        # Find the exact replication location based on http://wiki.openstreetmap.org/wiki/Planet.osm/diffs
        edition = delta - days
        aaa = "000"
        bbb = str(edition/1000).zfill(3)
        ccc = str(edition%1000).zfill(3)

        url =  osm_replication_url+aaa+"/"+bbb+"/"+ccc+".osc.gz"
        print '# Replication URL', url

        # Download the replication
        wget.download(url)

        # Unzip the file
        bash("gzip -d {}".format(ccc + ".osc.gz"))

        # Create an archive for the changesets
        edition_archive = zipfile.ZipFile("edition_{}.zip".format(ccc), 'w')

        for user in users:
            user = user.strip('\n')
            print '# Processing ' + user +"'s changes"
            bash('./osmfilter {}.osc --keep="@user={}" -o={}.osm'.format(ccc, user, user))
            edition_archive.write('{}.osm'.format(user), compress_type=compression)

        # Cleanup
        bash("rm {}.*".format(user))

        edition_archive.close()

        # Process previous edition number
        days-=1