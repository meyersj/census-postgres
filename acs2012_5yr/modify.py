import string, csv


file_id = 0
tbl_id = 1
seq_num = 2
line_num = 3
start_pos = 4
tot_cell_tbl = 5
tot_cell_seq = 6
tbl_title = 7
subj_area = 8


def build_table_names():
    names_dict = {}
    with open('scratch/Sequence_Number_and_Table_Number_Lookup.txt', 'r') as f:
        reader = csv.reader(f)
        
        with open('scratch/table_names.txt', 'wb') as fout:
            write = csv.writer(fout)
            
            for row in reader:
                
                if row[start_pos] != ' ':
                    tmp_id = row[tbl_id]
                    names_dict[tmp_id] = {}
                    names_dict[tmp_id]['title'] = row[tbl_title].replace(' ', '_').replace(',', '')
                    names_dict[tmp_id]['fields'] = {}
                    fout.write(tmp_id + '( ' + row[tbl_title].replace(' ', '_').replace(',', '') + ' )\n')  
                elif row[line_num] != ' ': 
                    seq = row[line_num]  
                    #print seq + ':' + str(string.find(seq, '.'))
                    if string.find(seq, '.') == -1:
                        if len(seq) == 1:
                            seq = '00' + seq
                        elif len(seq) == 2:
                            seq = '0' + seq
                        

                        names_dict[tmp_id]['fields'][tmp_id + seq] = row[tbl_title].replace(' ', '_').replace(',', '')  
                        fout.write('   ' + tmp_id + seq + '( ' + row[tbl_title].replace(' ', '_').replace(',', '') + ' )\n')
                        
    return names_dict
                        
def build_named_views(names_dict):                       
    create_view = 'CREATE VIEW acs2012_5yr.{0} AS SELECT\n'

  

    with open('view_stored_by_tables.sql', 'r') as f:
        lines = f.read().splitlines()
                        
    with open('scratch/view_stored_by_tables_named.sql', 'w') as fout:
        for line in lines:
            
            if string.find(line, 'CREATE VIEW') != -1:
                acs = line.split()[2].split('.')[1]
                #fout.write(drop_view.format(acs[1]))
                if acs[-3:] != 'moe':
                    print acs
                    fout.write(create_view.format(names_dict[acs]['title']))
                    #fout.write(line + '\n')
                else:
                    fout.write(create_view.format(acs))
            
            elif string.find(line, 'geoid,') != -1:
                #pass
                fout.write(line + '\n')
                fout.write('substring(geoid from 8 for length(geoid) - 7) AS fips,\n')
            elif line[0:4] == 'FROM':
                fout.write(line + '\n')
            
            #convert field names to titles
            else:
                fout.write(line + '\n')
            
            #fout.write(line + '\n')

            #if line == 'geoid,':
            #    fout.write('substring(geoid from 8 for length(geoid) - 7) AS fips,\n')


















def open_summary_file():
    with open('scratch/Sequence_Number_and_Table_Number_Lookup.txt', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            
            if row[subj_area] != '':
                print row[tbl_id] + ' ' + row[tbl_title] + ' ' + row[subj_area]



#Modify view_stored_tables.sql to strip fips out of geoid and build view_stored_by_tables_fips_edit.sql
def view_fips_edit():
    with open('view_stored_by_tables.sql', 'r') as f:
        lines = f.read().splitlines()

    with open('view_stored_by_tables_fips_edit.sql', 'w') as fout:
        for line in lines:
            fout.write(line + '\n')

            if line == 'geoid,':
                fout.write('substring(geoid from 8 for length(geoid) - 7) AS fips,\n')


#Build drop_view_stored_by_tables.sql by getting each view name and building DROP command
def drop_views():
    drop_view = "DROP VIEW IF EXISTS {0};\n"

    with open('view_stored_by_tables.sql', 'r') as f:
        lines = f.read().splitlines()
        
    with open('drop_view_stored_by_tables.sql', 'w') as fout:
        for line in lines:
            if string.find(line, 'CREATE VIEW') != -1:
                acs = line.split()[2].split('.')
                fout.write(drop_view.format(acs[1]))


#Build import_sequences.txt from list of tables
def build_import_seq():
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

if __name__ == '__main__':
    names = build_table_names()
    build_named_views(names)
    
    #open_summary_file()
