###################################################################
## Description: This script processes the data collected from
##              DownloadData.py and fuses into both a CSV and an Rda.
###################################################################

###################################################################
## Getting user arguments
###################################################################

args = commandArgs(trailingOnly=TRUE)

if (length(args)<2) {
  N_missing = 2 - length(args)
  cat(
    paste("This script fuses all CSV created by DownloadData.py into one",
          "", "Arguments:", "First argument is the Directory were the output of DownloadData.py is kept and the second one is the directory were the resulting CSV and Rda of this program will be created.",
          "",
          "Example: Rscript data Processed_data",
          sep="\n", end="\n")
    )
  stop(paste("Missing", N_missing,"arguments"))
}

###################################################################
## Set directory with CSVs from DownloadData.py and
## output directory
###################################################################

DataDirectory=args[1]

OutputDirectory=args[2]

###################################################################
## Loading dependencies
###################################################################

library(tibble)
library(dplyr)
library(tidyr)
library(plyr)

###################################################################
## Creating output directory and loading
## CSV files obtained from DownloadData.py into one dataframe
###################################################################

f <- list.files(file.path(DataDirectory), pattern = "Accidentes_")
df <- read.csv(file.path(DataDirectory,f[1]), sep=";")

for(i in f[-c(1)]){
  d <- read.csv(file.path(DataDirectory,i), sep=";")
  finalData <- rbind(df, d)
  df <- finalData
}

rm(finalData)

###################################################################
## Seting data to its corresponding type and
## translating it to English.
###################################################################

DF <- df %>% mutate(Lloc = as.factor(Lloc),
                    Grau_Perill = revalue(as.factor(Grau_Perill),
                                          c("Desconegut" = "Unknown",
                                            "Fora periode de predicció" = "Out of prediction period",
                                            "Sense predicció" = "No prediction")
                                          ),
                    Tipus_Desencadenant = revalue(
                                            as.factor(Tipus_Desencadenant),
                                            c("Desconegut" = "Unknown",
                                              "Desconegut (null)" = "Unknown",
                                              "Placa (PL)" = "Slab",
                                              "Puntual (PU)" = "Point Release")
                                                  ),
                    Origen = revalue(as.factor(Origen), c(
                      "Desconegut" = "Unknown"
                    )),
                    Mida = as.numeric(Mida),
                    Membres = as.numeric(Membres),
                    Arrossegats = ifelse(is.na(as.numeric(Arrossegats)),
                                         -1, as.numeric(Arrossegats)),
                    Ferits = ifelse(is.na(as.numeric(Ferits)),-1, 
                                    as.numeric(Ferits)),
                    Morts = ifelse(is.na(as.numeric(Morts)),-1, 
                                   as.numeric(Morts)),
                    Activitat = revalue(as.factor(Activitat), c(
                                                                "Alpinisme"="Mountaineerin",
                                                                "Altres"="Others",
                                                                "Desconegut"="Unknown",
                                                                "Esquí de muntanya"="Skimo",
                                                                "Esquí de pista" = " On-piste skiing",
                                                                "Esquí fora pista" = "Off-piste skiing",
                                                                "Excursionisme" = "Hiking",
                                                                "Moto de neu" = "Snow bike",
                                                                "Raquetes" = "Rackets",
                                                                "Taula de muntanya" = "Mountainboarding",
                                                                "Taula fora pista" = "Freeride",
                                                                "Treballant" = "Working"
                                                                ))
                    ) %>% separate(Data, into = c("Dia", "Mes", "Any"), sep = "/") %>% 
  arrange(as.numeric(Any)) %>% 
  mutate(Dia = as.factor(Dia), Mes = as.factor(Mes), Any = as.factor(Any)) %>% 
  rename(
    c(
      "Dia" = "Day",
      "Mes" = "Month",
      "Any" = "Year",
      "Lloc" = "Location",
      "Grau_Perill" = "Danger_Score",
      "Tipus_Desencadenant" = "Trigger_Type",
      "Origen" = "Origin",
      "Mida" = "Size",
      "Membres" = "Members",
      "Arrossegats" = "Dragged",
      "Ferits" = "Hurt",
      "Morts" = "Dead",
      "Activitat" = "Activity"
      )
  )

###################################################################
## Saving data in both CSV and RDA formats.
###################################################################

dir.create(OutputDirectory)

save(DF, file = file.path(OutputDirectory,"data.Rda"))

write.csv(DF, file = file.path(OutputDirectory,"Alud_accidents.csv"))




