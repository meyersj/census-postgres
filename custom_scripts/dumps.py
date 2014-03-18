"""
author: Jeffrey Meyers
for: TriMet
created: 3/18/2014

script will either make a dump of census schemas or restore previously dumped schemas

values hardcoded in:

[schema names]
acs2012_1yr
acs2012_3yr
acs2012_5yr

[host]
maps2.trimet.org

[database]
trimet

to run:

python dumps.py <method> <directory>

<method> accepts 'dump' or 'restore'
<directory> path to folder where dumps should be sent or restored from

"""

import sys
import logging
import os.path
import subprocess

logging.basicConfig(level=logging.DEBUG)

def dump(directory, schemas):
    pg_dump = 'pg_dump -U geoserve -h maps2.trimet.org -f {0} -n {1} -F tar trimet'
    output = 'maps2_{0}.tar'
    
    for schema in schemas:
        output_file = os.path.join(directory, output.format(schema))
        command = pg_dump.format(output_file, schema)
        logging.info("dumping " + schema)
        try:
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError:
            logging.error("failed to dump "+schema+" with '"+command+"'")


def restore(directory, schemas):
    pg_restore = 'pg_restore -U geoserve -h maps2.trimet.org -d trimet -F tar {0}'
    geom_command = 'psql -h maps2.trimet.org -U geoserve -d trimet -c "GRANT INSERT ON TABLE public.geometry_columns TO tmpublic;GRANT DELETE ON TABLE public.geometry_columns TO tmpublic;"'
    dump_file = 'maps2_{0}.tar'
    
    for schema in schemas:
        input_file = os.path.join(directory, dump_file.format(schema))
        if not os.path.isfile(input_file):
            logging.error("could not find file "+input_file)    
        else:
            logging.info("found file to restore "+input_file)
            command = pg_restore.format(input_file)
            try:
                subprocess.check_call(command, shell=True)
            except subprocess.CalledProcessError:
                logging.error("failed to restore "+schema+" with '"+command+"'")   
    try:
        subprocess.check_call(geom_command, shell=True)
    except subprocess.CalledProcessError:
        logging.error("failed to add priviliges on public.geometry_columns")   

def main(method, directory, schemas):
    if method == "dump":
        dump(directory, schemas)
    elif method == 'restore':
        restore(directory, schemas)
    else:
        logging.error(method + " is not a valid method")

if __name__ == '__main__':
    schemas = ['acs2012_1yr', 'acs2012_3yr', 'acs2012_5yr', 'census_geo', 'census_working'] 
    if len(sys.argv) != 3:
        logging.error("incorrect number of parameters, expects 'python dumps.py <method> <directory>'")
    else: 
        method = sys.argv[1]
        directory = sys.argv[2]
        if os.path.isdir(directory):
            main(method, directory, schemas)
        else:
            logging.error("directory provided does not exist")
