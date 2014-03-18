--Copy only Oregon and Washington geography files into tmp_geoheader

COPY acs2012_1yr.tmp_geoheader FROM 'C:/temp/census/ORWA_All_Geographies_acs2012_1yr/g20121or.txt' WITH ENCODING 'latin1';
COPY acs2012_1yr.tmp_geoheader FROM 'C:/temp/census/ORWA_All_Geographies_acs2012_1yr/g20121wa.txt' WITH ENCODING 'latin1';
