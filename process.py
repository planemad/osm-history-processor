import argparse
import wget
import subprocess
import os.path
import zipfile

# Import zlib for compression
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED
    
# Define arguments for the parser
parser = argparse.ArgumentParser(description='History processor for Openstreetmap')
parser.add_argument('edition', metavar='N', type=int,
                   help='Latest edition number')
args = parser.parse_args()

# Utility function to run shell commands
def bash(command):
    "Runs a command in shell"
    subprocess.call(command, shell=True)
    return

# OSM repication server url and data team users
osm_replication_url = "http://planet.osm.org/replication/day/000/000/"
users = ['Rub21', 'ediyes', 'RichRico', 'Luis36995', 'dannykath', 'andygol', 'shravan91', 'ruthmaben', 'abel801', 'samely', 'calfarome', 'srividya_c', 'PlaneMad']
edition_steps = 7

##

if __name__ == "__main__":
    
    # Create a dir for the files
    bash("mkdir files")
    bash("cd files")
    while edition_steps>=0:
        
        # Set the current edition number
        edition = str(args.edition - edition_steps) 

        #Download the replication edition
        wget.download(osm_replication_url + edition + ".osc.gz")
        
        #Unzip the file
        bash("gzip -d {}".format(edition + ".osc.gz"))

        #Convert from osc to 05m format
        bash("./osmconvert {}.osc > {}.05m".format(edition, edition))

        #Create a zip archive for the changesets
        edition_archive = zipfile.ZipFile("edition_{}.zip".format(edition), 'w')

        for user in users:
            bash('./osmfilter {}.osc --keep="@user={}" -o={}.osm'.format(edition, user, user))
            edition_archive.write('{}.osm'.format(user), compress_type=compression)
        
        # Cleanup
        bash("rm {}.*".format(user))

        edition_archive.close()
        
        #Process previous edition number
        edition_steps-=1
        
    #Package all edition archives
    