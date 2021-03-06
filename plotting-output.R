#!/usr/bin/env Rscript

# Copyright 2013 
# Mostly Helene Genet & Colin Tucker, with some touchups by Tobey Carman
# Spatial Ecology Lab
# University of Alaska Fairbanks

# This script is designed to ...
# inputs...
# outputs...

library(argparse)

d <- paste('This script reads a whole bunch of csv files that werte generated',
           'with output-extract.R. This script plots the variables and places',
           'the resulting plots in a folder (identified by the "--output-id"',
           'option).', sep=' ')
parser <- ArgumentParser(description=d)
                          # Looks like some of the fancier options like the
                          # formatter_class are not available yet...
                         
h <- paste('A path (absolute or relative) to a directory of csv files that',
           'were generated using output-extract.R.', sep=' ')
            
parser$add_argument('--generated-csv-dir', required=TRUE, 
                    metavar='PATH', help=h)

h <- paste('A unique name to indentify this set of generated plots (pdfs)',
           'All the generated plots will end up in a folder with this name in',
           'the current directory (wherever you call this script from).', 
           sep=' ')
parser$add_argument('--output-id', metavar='ID', help=h)
       
args <- parser$parse_args()             

# save the location the script was called from...
callingdir <- getwd()

# working directory
print("Setting the working directory...")
setwd(args$generated_csv_dir)

# ENTER MODEL VERSION == subdirectory to output to
print("Setting up the directory we will output pdfs into...")
dir.create(file.path(callingdir, args$output_id))

# --- N CYCLE PLOTS ---
pdf(file.path(callingdir, args$output_id, "Ncycle.pdf"))
par(mfrow=c(3,4), oma=c(0.1,0.1,0,0), mai=c(.3,.3,.25,.25), cex.main=0.9, cex.axis=0.75)
nmob<-read.csv('./bgc_yly_NMOBIL_eq.csv')
plot(nmob[102:2081,2],nmob[102:2081,4], type="l", xlab="", ylab="", main="Nmobile")
nreso<-read.csv('./bgc_yly_NRESORB_eq.csv')
plot(nreso[102:2081,2],nreso[102:2081,4], type="l", xlab="", ylab="", main="Nresorb")
nupsall<-read.csv('./bgc_yly_NUPTAKESALL_eq.csv')
plot(nupsall[102:2081,2],nupsall[102:2081,4], type="l", xlab="", ylab="", main="Nuptakesall")
nupl<-read.csv('./bgc_yly_NUPTAKEL_eq.csv')
plot(nupl[102:2081,2],nupl[102:2081,4], type="l", xlab="", ylab="", main='Nuptakel')
vns<-read.csv('./bgc_yly_VEGNSUM_eq.csv')
plot(vns[102:2081,2],vns[102:2081,4], type="l", xlab="", ylab="", main= "VegNsum")
nnmin<-read.csv('./bgc_yly_NETNMIN_eq.csv')
plot(nnmin[102:2081,2],nnmin[102:2081,4], type="l", xlab="", ylab="", main="NetNmin")
ltrN<-read.csv('./bgc_yly_LTRFALNALL_eq.csv')
plot(ltrN[102:2081,2],ltrN[102:2081,4], type="l", xlab="", ylab="", main="LtrfalNall")
avln<-read.csv('./bgc_yly_AVLNSUM_eq.csv')
plot(avln[102:2081,2],avln[102:2081,4], type="l", xlab="", ylab="", main="AvlNsum")
avlnin<-read.csv('./bgc_yly_AVLNINPUT_eq.csv')
plot(avlnin[102:2081,2],avlnin[102:2081,4], type="l", xlab="", ylab="", main="AvlNinput")
avlnlost<-read.csv('./bgc_yly_AVLNLOST_eq.csv')
plot(avlnlost[102:2081,2],avlnlost[102:2081,4], type="l", xlab="", ylab="", main="AvlNlost")
ornlost<-read.csv('./bgc_yly_ORGNLOST_eq.csv')
plot(ornlost[102:2081,2],ornlost[102:2081,4], type="l", xlab="", ylab="", main="OrgNlost")
dev.off()

# TEST C CYCLE
pdf(file.path(callingdir, args$output_id, "Ccycle.pdf"))
par(mfrow=c(3,4), oma=c(0.1,0.1,0,0), mai=c(.3,.3,.25,.25), cex.main=0.9, cex.axis=0.75)
nep<-read.csv('./bgc_yly_NEP_eq.csv')
plot(nep[102:2081,2],nep[102:2081,4], type="l", xlab="", ylab="", main="NetEcoProd")
npp<-read.csv('./bgc_yly_NPPALL_eq.csv')
plot(npp[102:2081,2],npp[102:2081,4], type="l", xlab="", ylab="", main="NetPrimProd")
gpp<-read.csv('./bgc_yly_GPPALL_eq.csv')
plot(gpp[102:2081,2],gpp[102:2081,4], type="l", xlab="", ylab="", main="GrsPrimProd")
vcs<-read.csv('./bgc_yly_VEGCSUM_eq.csv')
plot(vcs[102:2081,2],vcs[102:2081,4], type="l", xlab="", ylab="", main="VegCsum")
ltrC<-read.csv('./bgc_yly_LTRFALCALL_eq.csv')
plot(ltrC[102:2081,2],ltrC[102:2081,4], type="l", xlab="", ylab="", main="LtrfalCall")
somcs<-read.csv('./bgc_yly_SOMCSHLW_eq.csv')
plot(somcs[102:2081,2],somcs[102:2081,4], type="l", xlab="", ylab="", main="SOMCSHLW")
somcd<-read.csv('./bgc_yly_SOMCDEEP_eq.csv')
plot(somcd[102:2081,2],somcd[102:2081,4], type="l", xlab="", ylab="", main="SOMCDEEP")
somcma<-read.csv('./bgc_yly_SOMCMINEA_eq.csv')
plot(somcma[102:2081,2],somcma[102:2081,4], type="l", xlab="", ylab="", main="SOMCMINEA")
somcmc<-read.csv('./bgc_yly_SOMCMINEC_eq.csv')
plot(somcmc[102:2081,2],somcmc[102:2081,4], type="l", xlab="", ylab="", main="SOMCMINEC")
rhm<-read.csv('./bgc_yly_RHMOIST_eq.csv')
plot(rhm[102:2081,2],rhm[102:2081,4], type="l", xlab="", ylab="", main="RHMOIST")
rhq<-read.csv('./bgc_yly_RHQ10_eq.csv')
plot(rhq[102:2081,2],rhq[102:2081,4], type="l", xlab="", ylab="", main="RHQ10")
soillcn<-read.csv('./bgc_yly_SOILLTRFCN_eq.csv')
plot(soillcn[102:2081,2],soillcn[102:2081,4], type="l", xlab="", ylab="", main="SoilLtrFCN")
dev.off()

# TEST ENV VARs
pdf(file.path(callingdir, args$output_id, "EnvVar.pdf"))
par(mfrow=c(3,4), oma=c(0.1,0.1,0,0), mai=c(.3,.3,.25,.25), cex.main=0.9, cex.axis=0.75)
snow<-read.csv('./env_yly_SNOWFALL_eq.csv')
plot(snow[102:2081,2],snow[102:2081,5], type="l", xlab="", ylab="", main="SnowThick")
rain<-read.csv('./env_yly_RAINFALL_eq.csv')
plot(rain[102:2081,2],rain[102:2081,5], type="l", xlab="", ylab="", main="Rainfall")
EET<-read.csv('./env_yly_EETTOTAL_eq.csv')
plot(EET[102:2081,2],EET[102:2081,5], type="l", xlab="", ylab="", main="EETTotal")
PET<-read.csv('./env_yly_PETTOTAL_eq.csv')
plot(PET[102:2081,2],PET[102:2081,5], type="l", xlab="", ylab="", main="PETTotal")
Tair<-read.csv('./env_yly_TAIR_eq.csv')
plot(Tair[102:2081,2],Tair[102:2081,5], type="l", xlab="", ylab="", main="Tair")
Tsoil<-read.csv('./env_yly_SOILTAVE_eq.csv')
plot(Tsoil[102:2081,2],Tsoil[102:2081,5], type="l", xlab="", ylab="", main="SoilTAve")
soilvwc<-read.csv('./env_yly_SOILVWC_eq.csv')
plot(soilvwc[102:2081,2],soilvwc[102:2081,5], type="l", xlab="", ylab="", main="SoilVWC")
rzthaw<-read.csv('./env_yly_RZTHAWPCT_eq.csv')
plot(rzthaw[102:2081,2],rzthaw[102:2081,5], type="l", xlab="", ylab="", main="RootZoneThawPct")
ALD<-read.csv('./env_yly_ALD_eq.csv')
plot(ALD[102:2081,2],ALD[102:2081,5], type="l", xlab="", ylab="", main="ActiveLayerDepth")
dev.off()






















