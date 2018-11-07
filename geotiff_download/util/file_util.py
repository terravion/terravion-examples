import os
import logging
import json
import traceback
import re
import requests
import time
timeout_seconds = 1000

def check_duplicate_block_name(block_dic):
    block_name_list = []
    block_id_list = []

    for block_id in block_dic:
        block_name_list.append(block_dic[block_id]['block_name'])
        block_id_list.append(block_id)

    if len(tuple(set(block_name_list))) == len(tuple(set(block_id_list))):
        return None
    else:
        return True

def clean_filename(filename):
    return re.sub("[!|*'();:@&=+$,/?# [\]]", '-', filename)

def run_download_file(url, outfilename):
    r = requests.get(url, stream=True, timeout=timeout_seconds, verify=False)

    if r.status_code == 200:
        with open(outfilename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        raise Exception('status_code error', r.status_code)

    return outfilename


def download_file(url, outfilename):
    log = logging.getLogger(__name__)
    error_log_list = []
    download_try_limit = 5
    download_time_elapsed = 0
    download_complete = False
    kill_download_thread = False

    for attempt in range(download_try_limit):
        try:
            log.debug('download_url:'+ url)
            log.debug('download_filename:'+ outfilename)
            run_download_file(url, outfilename)

        except:
            # thread_a.stop()
            # thread_b.stop()
            log.debug("download stuck?")
            error_log_list.append(str(traceback.format_exc()))

            if os.path.isfile(outfilename):
                os.remove(outfilename)
            time.sleep(5)
            continue

        if os.path.isfile(outfilename):
            return outfilename

    raise Exception('download failed', json.dumps(error_log_list))


class DownloadingReport(object):

    def __init__(self, csv_filename=None):
        self.csv_filename = csv_filename
        self.csv_header_list = ['output_filename', 'status',
                                'request_url', 'download_url',
                                'timestamp', 'message']
        self.download_record_list = []
        self.log = logging.getLogger(__name__)
    def insert_download_result(self, download_record):
        self.download_record_list.append(download_record)

    def write_csv_file(self, csv_filename=None):
        if csv_filename and not self.csv_filename:
            self.csv_filename = output_csv

        if self.download_record_list:
            with open(self.csv_filename, 'wb') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow(self.csv_header_list)

                for download_record in self.download_record_list:
                    output_filename = None
                    status = None
                    download_url = None
                    message = None
                    timestamp = None
                    request_url = None

                    if 'output_filename' in download_record:
                        output_filename = download_record['output_filename']

                    if 'status' in download_record:
                        status = download_record['status']

                    if 'download_url' in download_record:
                        download_url = download_record['download_url']

                    if 'message' in download_record:
                        message = download_record['message']

                    if 'timestamp' in download_record:
                        timestamp = download_record['timestamp']

                    if 'request_url' in download_record:
                        request_url = download_record['request_url']

                    csv_writer.writerow(
                        [output_filename, status,
                         request_url, download_url, timestamp,
                         message.replace('\n', ' ').replace('\r', '')])

    def print_download_record_list(self):
        if self.download_record_list:
            self.log.debug('---------------------------------------------------------------------------------------')
            self.log.debug(' '.join(self.csv_header_list))

            for download_record in self.download_record_list:
                output_filename = None
                status = None
                download_url = None
                message = None
                timestamp = None
                request_url = None

                if 'output_filename' in download_record:
                    output_filename = download_record['output_filename']

                if 'status' in download_record:
                    status = download_record['status']

                if 'download_url' in download_record:
                    download_url = download_record['download_url']

                if 'message' in download_record:
                    message = download_record['message']

                if 'timestamp' in download_record:
                    timestamp = download_record['timestamp']

                if 'request_url' in download_record:
                    request_url = download_record['request_url']
                self.log.debug(' '.join([output_filename, status, download_url, timestamp, message]))
