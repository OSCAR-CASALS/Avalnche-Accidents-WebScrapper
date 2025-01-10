from src.ScrappingFunctions import GetInformation, getCoordinates
import time
import os

import argparse

###################################################################
# Collect user Input
###################################################################

parser = argparse.ArgumentParser(
    description="Collects accidents from a certain season from ACNA's avalanche database avalaible at their oficial website."
    )

# Es defineixen els diferents parametres que pot definir el usuari.
parser.add_argument("-y","--years", nargs="+", type=str, required=True, help="Seasons from which to collect information")
parser.add_argument("-o", "--output", type=str, required=False, default="data", help="Output directory where CSV files will be created")
args = parser.parse_args()

Seasons = args.years

OutputDirectory = args.output

print("Seasons:", Seasons)

print("Output directory:", OutputDirectory)

###################################################################
# Collect data
###################################################################

# Create directory to hold csv
if not os.path.exists("data"):
    os.mkdir(OutputDirectory)

for i in Seasons:
    GetInformation(i, OutputDirectory)
    time.sleep(2)