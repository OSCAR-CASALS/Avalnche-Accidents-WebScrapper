# ACNA accidents scrapper

## Description

Web Scrapping program used to extract data from ACNA's accident database at
https://www.acna.es/estadisticas-de-accidentes/, in specific the iframe included in set web page.

## Instalation

To download the repository the command git clone can be used:

```
git clone https://github.com/OSCAR-CASALS/Avalnche-Accidents-WebScrapper.git
```

To install the python dependencies required to run this web scrapper the requirements.txt file included in the
repository can be used as following:

```
pip install -r requirements.txt
```

To aquire the R dependencies required to process data the script install.R can be used as following:

```
Rscript install.R
```

## Usage

First execute DownloadData.py specifiying the seasons you want to extract information
from with --years (or -y) argument and the output directory with argument --output 
(or -o) to create different CSV files with the entries of each season at ACNA's database.

```
python DownloadData.py --years "202324" "202223" "202122" --output data
```

Then use the script ProcessData.R to join all csv into one, process data, and 
translate it to english.

```
Rscript ProcessData.R data Processed_data
```

## Version

1.1
