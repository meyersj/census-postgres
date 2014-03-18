--Copy only Oregon and Washington geography files into tmp_geoheader

COPY acs2012_3yr.tmp_geoheader FROM 'C:/temp/census/ORWA_All_Geographies_acs2012_3yr/g20123or.txt' WITH ENCODING 'latin1';
COPY acs2012_3yr.tmp_geoheader FROM 'C:/temp/census/ORWA_All_Geographies_acs2012_3yr/g20123wa.txt' WITH ENCODING 'latin1';
