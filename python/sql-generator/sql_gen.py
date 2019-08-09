import os
import csv


def append_db_cursor(sql_rows, header):
    sql_rows.append('\nDECLARE @cnt INT = 0')
    for col in header:
        sql_rows.append('DECLARE @' + col + ' NVARCHAR(200)')
    sql_rows.append('DECLARE db_cursor CURSOR FOR')
    sql_rows.append('SELECT {} FROM @TempTable'.format(','.join(header)))
    sql_rows.append('OPEN db_cursor')
    fetch_sql = 'FETCH NEXT FROM db_cursor INTO '
    for col in header:
        fetch_sql = fetch_sql + '@' + col + ','
    fetch_sql = fetch_sql[:-1]
    sql_rows.append(fetch_sql)
    sql_rows.append('WHILE @@FETCH_STATUS = 0')
    sql_rows.append('BEGIN')
    sql_rows.append('  SET @cnt = @cnt + 1')
    sql_rows.append('  ')
    sql_rows.append('  ')
    sql_rows.append('  ')
    sql_rows.append('  ' + fetch_sql)
    sql_rows.append('END')
    sql_rows.append('CLOSE db_cursor')
    sql_rows.append('DEALLOCATE db_cursor')


def csv_to_insert(csv_input, sql_output, count=0, table='@TempTable', with_cursor=True):
    sql_rows = []
    with open(csv_input, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, skipinitialspace=True)
        header = next(csv_reader)
        temp_sql = "\nDECLARE {} TABLE ({} NVARCHAR(200))".format(table, ' NVARCHAR(200),'.join(header))
        print(temp_sql)
        sql_rows.append(temp_sql)
        sql_head = "INSERT INTO {} ({}) VALUES ".format(table, ', '.join(header))
        print(sql_head)
        sql_rows.append(sql_head)
        data_rows = []
        row_no = 0
        for row in csv_reader:
            str_row = []
            for item in row:
                str_row_item = "'{}'".format(item.replace('\'', '\'\''))
                if str_row_item == "'NULL'":
                    str_row_item = 'NULL'
                str_row.append(str_row_item)

            if 0 < count and count != len(str_row):
                raise Exception('row count {} is unexpected, expected to be {}. {}'.format(len(str_row), count, ','.join(str_row)))
            data_row = "  ({}),".format(', '.join(str_row))
            data_rows.append(data_row)

            row_no = row_no + 1

        for i in range(len(data_rows)):
            data_row = data_rows[i]
            if i == (len(data_rows) - 1):
                data_row = data_row[:-1]
                sql_rows.append(data_row)
            else:
                sql_rows.append(data_row)

    if with_cursor:
        append_db_cursor(sql_rows, header)

    if os.path.exists(sql_output):
        os.remove(sql_output)
    with open(sql_output, 'a') as file:
        for sql_row in sql_rows:
            print(sql_row)
            file.write(sql_row + '\n')


def csv_to_dict(file):
    with open(file, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            print(row)


csv_to_insert('csv/permits.csv', 'permits_cursor.sql')
csv_to_insert('csv/equipment-type.csv', 'equipment-types-cursor.sql')
csv_to_insert('csv/frequency.csv', 'frequency-cursor.sql')
csv_to_insert('csv/lookup.csv', 'lookup-cursor.sql')
csv_to_insert('csv/waste-type.csv', 'waste-types-cursor.sql')
csv_to_insert('csv/contact.csv', 'contact-temptable.sql', 18, '@TempContact', False)
csv_to_insert('csv/contact-permit.csv', 'contact-permit-temptable.sql', 0, '@TempPermitContact')

csv_to_insert('csv/hauler.csv', 'hauler-temptable.sql', 6, '@TempHauler')


