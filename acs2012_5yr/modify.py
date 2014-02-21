import string


with open('view_stored_by_tables.sql', 'r') as f:
    lines = f.read().splitlines()

with open('view_stored_by_tables_fips_edit.sql', 'w') as fout:
    for line in lines:
        fout.write(line + '\n')

        if line == 'geoid,':
            fout.write('substring(geoid from 8 for length(geoid) - 7) AS fips,\n')










"""Build drop_view_stored_by_tables.sql by getting each view name and building DROP command"""
def build_views():
    drop_view = "DROP VIEW IF EXISTS {0};\n"

    with open('view_stored_by_tables.sql', 'r') as f:
        lines = f.read().splitlines()
        


    with open('drop_view_stored_by_tables.sql', 'w') as fout:
        for line in lines:
            if string.find(line, 'CREATE VIEW') != -1:
                acs = line.split()[2].split('.')
                fout.write(drop_view.format(acs[1])








"""Build import_sequences.txt from list of tables"""

def build import_seq():
    command = "COPY acs2012_5yr.tmp_seq{0} FROM '{1}{2}' WITH CSV;\n"

    nbg = "C:/temp/census/All_Not_Tracts_Block_Groups/"
    bgo = "C:/temp/census/All_Tracts_Block_Groups_Only/"

    with open('files.txt', 'r') as f:
        files = f.read().splitlines()


    with open('files.sql', 'w') as fout:
        for f in files:
            pre = f[0:6]
            post = f[-7:] 
            seq_num = f[-11:-7]
            seq = seq_num
            if f[0] == 'm' :
                seq = seq + '_moe'

            ore = pre + 'or' + seq_num + post
            wash = pre + 'wa' + seq_num + post

            ore_c1 = command.format(seq, nbg, ore)
            ore_c2 = command.format(seq, bgo, ore)
            wash_c1 = command.format(seq, nbg, wash)
            wash_c2 = command.format(seq, bgo, wash)
            
            fout.write(ore_c1)
            fout.write(ore_c2)
            fout.write(wash_c1)
            fout.write(wash_c2)
            
            print ore_c1, ore_c2, wash_c1, wash_c2

