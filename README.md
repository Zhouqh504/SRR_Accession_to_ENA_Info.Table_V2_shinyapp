# SRR_Accession_to_ENA_Info.Table_V2_shinyapp
This app is modified from TBtools function "SRRnum to ENA info. Table" for obtaining ENA links information based on SRR numbers.

web app URL：https://zhouqh.shinyapps.io/srr_accession_to_ena_info_table_v21/

NCBI only stores parts of SRR data in .sra format. DDBJ stroes less, while it contains most
data in .sra format with a few in .fastq format.
ENA database is the best one, which stores almost all short read sequencing data 
in SRA and Fastq format. To get the links requires some coding jobs. 
Thus, this function is developed. It takes a list of SRR numbers and return info. in ENA database.
To each SRR num, it would take about 3 seconds, so if the list is too long, for example, 
100 SRRnums, it would take almost 300 seconds, that is 5 minutes.
Enjoy it!               ------cited by zhouqh from CJ
