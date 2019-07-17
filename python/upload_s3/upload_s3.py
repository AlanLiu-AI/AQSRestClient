import logging
import boto3
import os
import ntpath
from botocore.exceptions import ClientError

file_uuids = {
    "McDonald-DSC8359.thumbnail.jpg" : '6A4E8CAD-BB0E-469D-8751-F04FE2F22645',
    "McDonald-DSC8359.jpg" : '2DB6470A-8523-4F65-BA4C-3D819285A7E5',
    "Black+Blue-dry-age-cellar.thumbnail.JPG" : '0483B999-7D08-4965-8046-2A76F4068BE4',
    "Black+Blue-dry-age-cellar.JPG" : 'E866A40E-F753-4C40-BB90-FC5354CB6BA6',
    "Salam Bombay.thumbnail.jpg" : '10A80659-60D6-4A94-BC22-2137DBEFC72F',
    "Salam Bombay.jpg" : 'C2403FED-F0E7-40CB-A19A-3D513F8A06A8',
    "Grease Trap installation Details.thumbnail.JPG" : 'CAB4FAE3-BED8-4E75-9A75-608EAF032416',
    "Grease Trap installation Details.mp4" : 'A04311D3-2F99-4BBC-8745-E8A88BF4A9CF',
    "Strata Grease Interceptors.thumbnail.JPG" : '9821C6DF-D983-47B2-A468-704A58487F9E',
    "Strata Grease Interceptors.mp4" : 'B263D724-4BC4-4B01-A224-360271FD15E6',
    "Stanley Environmental Solutions- Grease Trap Pumping.thumbnail.jpg" : '4126892E-C71D-40C5-BD51-1B7771D62367',
    "Stanley Environmental Solutions- Grease Trap Pumping.mp4" : '6E1D8C41-E286-4637-8780-F2B72D2A2356',
    "LinkoExchange_SampleDataImportExample_20180131.xlsx" : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    "Toddler dies after falling into Tim Hortons grease trap.docx" : '033df1b0-f4fb-4363-a96f-32e2771cc5b3',
    "Toddler dies after falling into Tim Hortons grease trap.pdf" : '18dab597-a45f-48a7-a989-55021e2c117b'
}

media_tyeps = {
    '.jpg': 'image/jpeg',
    '.mp4': 'video/mp4',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.pdf': 'application/pdf'
}

def get_files(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files


def bucket_exists(bucket_name):
    """Determine whether bucket_name exists and the user has permission to access it

    :param bucket_name: string
    :return: True if the referenced bucket_name exists, otherwise False
    """

    s3 = boto3.client('s3')
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.debug(e)
        return False
    return True


def upload(bucket_name, file_path):
    filename = ntpath.basename(file_path)
    file_extension = os.path.splitext(filename)[1]
    logging.debug(f'upload file {filename} to bucket {bucket_name} started...')
    key = '1001/1002/attachments/' + file_uuids[filename]
    media_type = media_tyeps[file_extension.lower()]
    metadata = {"ContentType": media_type, "ContentDisposition": "filename=" + filename}

    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).upload_file(file_path, key, ExtraArgs=metadata)
    logging.info(f'upload file {file_path} to bucket {bucket_name} with key: {key}, media type: {media_type}')


def main():
    """Exercise bucket_exists()"""

    # Assign this value before running the program
    bucket_name = 'linko-online-s3-dev'

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Check if the bucket exists
    if not bucket_exists(bucket_name):
        logging.info(f'{bucket_name} does not exist or '
                     f'you do not have permission to access it.')
        exit(-1)


    logging.info(f'{bucket_name} exists and you have permission to access it.')
    files = get_files('D:\\git\\linko\\temp\\attachment\\')

    for file in files:
        upload(bucket_name, file)


if __name__ == '__main__':
    main()