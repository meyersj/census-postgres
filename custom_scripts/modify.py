import string, csv, re, sys

file_id = 0
tbl_id = 1
seq_num = 2
line_num = 3
start_pos = 4
tot_cell_tbl = 5
tot_cell_seq = 6
tbl_title = 7
subj_area = 8

table_sizes = []
field_sizes = []

"""
#RETIRED#

def check_table(name):
    global table_sizes
    table_sizes.append(len(name) + 1)

def check_field(name):
    global field_sizes
    field_sizes.append(len(name) + 1)

def format_name(name):
    name = name.replace(' ', '_').replace('-', '_')
    name = re.sub(r'\W+', '', name)
    if name[0].isdigit():
        name = '_' + name
    return name

def build_table_names():
    names_dict = {}
    names_dict['fields'] = {}
    names_dict['titles'] = {}
    
    with open('scratch/Sequence_Number_and_Table_Number_Lookup.txt', 'r') as f:
        reader = csv.reader(f)
        with open('scratch/table_names.txt', 'wb') as fout:
            
            for row in reader:
                if row[start_pos] != ' ':
                    tmp_id = row[tbl_id]
                    names_dict[tmp_id] = {}
                    name = format_name(row[tbl_title]) 
                   
                    if len(name) + 1 > 63:
                        name = tmp_id
                    
                    names_dict['titles'][tmp_id] = name
                    fout.write(tmp_id + ' ' + name + '\n')  
                    writer.writerow([name, len(name) + 1, 'table'])
                
                elif row[line_num] != ' ': 
                    seq = row[line_num]  
                    if string.find(seq, '.') == -1:
                        if len(seq) == 1:
                            seq = '00' + seq
                        elif len(seq) == 2:
                            seq = '0' + seq
                        field_id = tmp_id + seq 
                        field = format_name(row[tbl_title])  
                        if len(field) + 1 > 63:
                            field = field_id
                        names_dict['fields'][field_id] = field  
                        #print names_dict['fields'][tmp_id + seq]
                        fout.write('-' + field_id + ' ' + field + '\n')
                        writer.writerow([field, len(field) + 1, 'field'])

    for key, value in names_dict['titles'].iteritems():    
        check_table(value)

    for key, value in names_dict['fields'].iteritems():
        check_field(value)

    return names_dict


def build_named_views(names_dict):                       
    create_view = 'CREATE VIEW acs2012_5yr.{0} AS SELECT\n'
    field = '{0} AS {1}{2}\n'
    
    with open('view_stored_by_tables.sql', 'r') as f:
        lines = f.read().splitlines()
                        
    with open('scratch/view_stored_by_tables_named.sql', 'w') as fout:
        fout.write('BEGIN;\n\n')
        for line in lines:
            if 'CREATE VIEW' in line:
                acs = line.split()[2].split('.')[1]
                if 'moe' not in acs:
                    fout.write(create_view.format(names_dict['titles'][acs]))
                else:
                    fout.write(create_view.format(acs))

            elif 'geoid,' in line:
                fout.write(line + '\n')
                fout.write('substring(geoid from 8 for length(geoid) - 7) AS fips,\n')
            
            elif ('FROM' in line) or (line == '') or ('JOIN' in line):
                fout.write(line + '\n')
            
            else:
                if ',' not in line:
                    field_alias = field.format(line, names_dict['fields'][line], '') 

                else:
                    index = line.find(',')
                    field_name = line[0:index]
                    field_ending = line[index:]
                    field_alias = field.format(field_name, names_dict['fields'][field_name], field_ending)

                fout.write(field_alias)
        
        fout.write('COMMIT;\n\n')


def open_summary_file():
    with open('docs/Sequence_Number_and_Table_Number_Lookup.txt', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            
            if row[subj_area] != '':
                print row[tbl_id] + ' ' + row[tbl_title] + ' ' + row[subj_area]

def drop_named_views():
    drop_view = "DROP VIEW IF EXISTS acs2012_5yr.{0};\n"

    with open('scratch/table_names.txt', 'r') as f:
        lines = f.read().splitlines()
        
    with open('scratch/drop_named_view_stored_by_tables.sql', 'w') as fout:
        for line in lines:
            if line[0] != '-':
                fout.write(drop_view.format(line.split()[1]))          

"""

#Modify view_stored_tables.sql to strip fips out of geoid and build view_stored_by_tables_fips_edit.sql
def view_fips_edit():
    with open('../acs2012_1yr/view_stored_by_tables.sql', 'r') as f:
        lines = f.read().splitlines()

    with open('../acs2012_1yr/view_stored_by_tables_fips_1yr.sql', 'w') as fout:
        for line in lines:
            fout.write(line + '\n')

            if line == 'geoid,':
                fout.write('substring(geoid from 8 for length(geoid) - 7) AS fips,\n')


#Build drop_view_stored_by_tables.sql by getting each view name and building DROP command
def build_drop_views():
    drop_view = "DROP VIEW IF EXISTS acs2012_5yr.{0};\n"

    with open('view_stored_by_tables.sql', 'r') as f:
        lines = f.read().splitlines()
        
    with open('drop_view_stored_by_tables.sql', 'w') as fout:
        for line in lines:
            if string.find(line, 'CREATE VIEW') != -1:
                acs = line.split()[2].split('.')
                fout.write(drop_view.format(acs[1]))



#Build import_sequences.txt from list of tables
def build_import_seq(year):
    command = "COPY {0}.tmp_seq{1} FROM '{2}{3}' WITH CSV;\n"
    summary_path = "C:/temp/census/ORWA_All_Geographies_acs2012_{0}yr/"
    seq_files = "acs2012_{0}yr_{1}seq.txt"
    import_seq = "import_sequences_orwa_{0}yr.sql"
    acs = "acs2012_{0}yr"

    seq_files_named = seq_files.format(year,"or")
    with open("scratch/" + seq_files_named,  'r') as f:
            or_files = f.read().splitlines()

    seq_files_named = seq_files.format(year,"wa")
    with open("scratch/" + seq_files_named,  'r') as f:
            wa_files = f.read().splitlines()

    import_seq_named = import_seq.format(year)
    with open('import_sequences_orwa_3yr.sql', 'w') as fout:
        for f in or_files:
            pre = f[0:6]
            post = f[-7:] 
            seq_num = f[-11:-7]
            seq = seq_num
            if f[0] == 'm' :
                seq = seq + '_moe'

            seq_command = command.format(acs.format(year), seq, summary_path.format(year), f)
            fout.write(seq_command)

        for f in wa_files:
            pre = f[0:6]
            post = f[-7:] 
            seq_num = f[-11:-7]
            seq = seq_num
            if f[0] == 'm' :
                seq = seq + '_moe'

            seq_command = command.format(acs.format(year), seq, summary_path.format(year), f)
            print seq_command
            fout.write(seq_command)

if __name__ == '__main__':
    
    #build_import_seq("3")
    #view_fips_edit()
