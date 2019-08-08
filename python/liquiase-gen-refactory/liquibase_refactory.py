import xml.etree.ElementTree as ET
import os

ET.register_namespace('', 'http://www.liquibase.org/xml/ns/dbchangelog')
ET.register_namespace('ext', 'http://www.liquibase.org/xml/ns/dbchangelog-ext')
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
ET.register_namespace('schemaLocation',
                      'http://www.liquibase.org/xml/ns/dbchangelog-ext http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-ext.xsd http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.6.xsd')

deprecated_tables = ['tCollectionMethod', 'tCollectionMethodType', 'tCopyOfRecord', 'tCopyOfRecordCertificate',
                     'tCtsEventType', 'tDataFormat', 'tDataOptionality', 'tDataSource',
                     'tDataSourceCollectionMethod', 'tDataSourceCtsEventType',
                     'tDataSourceMonitoringPoint', 'tDataSourceParameter', 'tDataSourceUnit',
                     'tFogExtractor', 'tFileType', 'tFileStore', 'tFileStoreData', 'tFileVersion', 'tFileVersionField',
                     'tFileVersionTemplate', 'tFileVersionTemplateField', 'tLimitBasis', 'tLimitType',
                     'tMonitoringPoint', 'tMonitoringPointParameter', 'tMonitoringPointParameterLimit',
                     'tImportTempFile', 'tParameter', 'tParameterGroup', 'tParameterGroupParameter',
                     'tReportElementCategory', 'tReportElementType', 'tReportFile', 'tReportPackage',
                     'tReportPackageElementCategory', 'tReportPackageElementType', 'tReportPackageTemplate',
                     'tReportPackageTemplateAssignment', 'tReportPackageTemplateElementCategory',
                     'tReportPackageTemplateElementType',
                     'tReportSample', 'tReportStatus', 'tRepudiationReason', 'tSample', 'tSampleFrequency',
                     'tSampleRequirement', 'tSampleResult', 'tSignatoryRequest', 'tSignatoryRequestStatus',
                     'tSystemField']


def reformat_xml(xml_file):
    with open(xml_file) as f:
        lines = f.readlines()

    lines[
        0] = '<databaseChangeLog xmlns="http://www.liquibase.org/xml/ns/dbchangelog" xmlns:ext="http://www.liquibase.org/xml/ns/dbchangelog-ext" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog-ext http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-ext.xsd http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.6.xsd">\n'
    lines.insert(0, '<?xml version="1.1" encoding="UTF-8" standalone="no"?>\n')

    new_lines = []
    for line in lines:
        new_lines.append(line.replace('type="datetimeoffset(0)"', 'type="datetimeoffset"'))

    with open(xml_file, "w") as f:
        f.writelines(new_lines)


def get_chang_set_id(change_set_node, first_child_node):
    old_change_set_id = change_set_node.attrib['id']
    if first_child_node.tag == '{http://www.liquibase.org/xml/ns/dbchangelog}createTable':
        change_set_id = "createTable_{}".format(first_child_node.attrib['tableName'])
    elif first_child_node.tag == '{http://www.liquibase.org/xml/ns/dbchangelog}addUniqueConstraint':
        change_set_id = "addUniqueConstraint_{}".format(first_child_node.attrib['constraintName'])
    elif first_child_node.tag == '{http://www.liquibase.org/xml/ns/dbchangelog}createIndex':
        change_set_id = "createIndex_{}".format(first_child_node.attrib['indexName'])
    elif first_child_node.tag == '{http://www.liquibase.org/xml/ns/dbchangelog}addPrimaryKey':
        change_set_id = "addPrimaryKey_{}".format(first_child_node.attrib['constraintName'])
    elif first_child_node.tag == '{http://www.liquibase.org/xml/ns/dbchangelog}addForeignKeyConstraint':
        change_set_id = "addForeignKeyConstraint_{}_{}".format(first_child_node.attrib['baseTableName'],
                                                               first_child_node.attrib['baseColumnNames'].replace(',',
                                                                                                                  "_"))
    else:
        print(change_set_node.tag, change_set_node.attrib, first_child_node.tag, first_child_node.attrib)
        change_set_id = old_change_set_id
    return change_set_id


def get_table_names(first_child_node):
    table_names = []
    if first_child_node.tag == '{http://www.liquibase.org/xml/ns/dbchangelog}createTable':
        table_names.append(first_child_node.attrib['tableName'])
    elif first_child_node.tag == '{http://www.liquibase.org/xml/ns/dbchangelog}addUniqueConstraint':
        table_names.append(first_child_node.attrib['tableName'])
    elif first_child_node.tag == '{http://www.liquibase.org/xml/ns/dbchangelog}createIndex':
        table_names.append(first_child_node.attrib['tableName'])
    elif first_child_node.tag == '{http://www.liquibase.org/xml/ns/dbchangelog}addPrimaryKey':
        table_names.append(first_child_node.attrib['tableName'])
    elif first_child_node.tag == '{http://www.liquibase.org/xml/ns/dbchangelog}addForeignKeyConstraint':
        table_names.append(first_child_node.attrib['baseTableName'])
        table_names.append(first_child_node.attrib['referencedTableName'])

    return table_names


def is_change_set_deprecated(table_names):
    for tableName in table_names:
        for deprecated_table in deprecated_tables:
            if deprecated_table.lower() == tableName.lower():
                return True
    return False


def filter_file(input_file, dist_file, exclude):
    tree = ET.parse(input_file)
    root = tree.getroot()

    removed_cnt = 0
    for change_set in root[::-1]:
        change_operation = change_set[0]

        table_names = get_table_names(change_operation)
        if len(table_names) < 1:
            print(change_set.tag, change_set.attrib, change_operation.tag, change_operation.attrib)
            raise Exception('Cannot extract table names')

        # print(change_set_id, table_names)

        is_deprecated = is_change_set_deprecated(table_names)

        if exclude == True and is_deprecated == True:
            # print(dist_file, ' exclude this change set on tables:', table_names, change_operation.tag, change_operation.attrib)
            removed_cnt = removed_cnt + 1
            root.remove(change_set)
        elif exclude == False and is_deprecated == False:
            # print(dist_file, ' exclude this change set on tables:', table_names, change_operation.tag, change_operation.attrib)
            removed_cnt = removed_cnt + 1
            root.remove(change_set)
        else:
            # print(dist_file, ' include this change set on tables:', table_names, change_operation.tag, change_operation.attrib)
            removed_cnt = removed_cnt

    print()
    tree.write(dist_file)
    reformat_xml(dist_file)
    return removed_cnt


def beautify(input_file, dist_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    for child in root:
        first_grand_child = child[0]

        change_set_id = get_chang_set_id(child, first_grand_child)
        if change_set_id == child.attrib['id']:
            print(child.tag, child.attrib, first_grand_child.tag, first_grand_child.attrib)
            raise Exception('Cannot extract table names')

        child.set('author', 'alan.liu')
        child.set('id', change_set_id)
        # print(change_set_id, table_names)

    print("{} file has {} changeset".format(dist_file, len(root)))
    tree.write(dist_file)
    reformat_xml(dist_file)


def reformat(input_file, target_file, exclude):
    temp_file = "{}.raw".format(input_file)
    removed_cnt = filter_file(input_file, temp_file, exclude)
    print(removed_cnt)
    print()

    beautify(temp_file, target_file)
    os.remove(temp_file)


reformat('generate-changelog.xml', 'initial_tables.xml', True)
reformat('generate-changelog.xml', 'deprecated_tables.xml', False)
