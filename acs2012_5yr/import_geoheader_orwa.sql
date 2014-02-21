--Copy only Oregon and Washington geography files into tmp_geoheader

COPY acs2012_5yr.tmp_geoheader FROM 'C:/temp/census/Oregon_All_Geographies_Tracts_Block_Groups_Only/g20125or.txt' WITH ENCODING 'latin1';
COPY acs2012_5yr.tmp_geoheader FROM 'C:/temp/census/Washington_All_Geographies_Tracts_Block_Groups_Only/g20125wa.txt' WITH ENCODING 'latin1';