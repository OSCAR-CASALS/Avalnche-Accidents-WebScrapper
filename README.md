# ACNA accidents scrapper

## Description

Web Scrapping program used to extract data from ACNA's accident database at
https://www.acna.es/estadisticas-de-accidentes/, in specific the iframe included in set web page.

## Usage

First execute DownloadData.py specifiying the seasons you want to extract information
from with --years (or -y) argument and the output directory with argument --output 
(or -o) to create different CSV with the entries of each season at ACNA's database.

```
python DownloadData.py --years "202324" "202223" "202122" --output data
```

Then use the script ProcessData.R to join all csv into one, process data, and 
translate it to english.

```
Rscript ProcessData.R data Processed_data
```

## Version

1.0