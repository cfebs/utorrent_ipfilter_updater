import urllib2
import os

class FilterDownloader(object):
    """ a class to get filter files and manipulate them """

    def __init__(self, url_list = [], download_path = 'downloads'):
        self.download_path = download_path 
        self.url_list = []
        self.file_queue = []

    def download_files(self):
        """
        loop through url list and download_file
        """
        for url in url_list:
            download_file(url)
    

    def download_file(self, url):
        """
        requests a remote file
            checks if the file exists first
            adds file pointer to the queue
        
        """
                
        try:
            response = urllib2.urlopen(url) 
        except URLError as e:
            # Log this
            return
        
        url = response.geturl()
        file_name = url.split('/')[-1] 
        file_path = os.path.join(self.download_path, file_name)

        # add the pointer to the queue to be processed
        self.file_queue.append(file_path)

        if (self.file_exists(file_path)):
            # do not need to download
            return

        f = open(file_path, 'wb')
        f.write(response.read())
        f.close()

        
    def file_exists(self, file_path):
        """
        does a file exist by name
        """
        try:
            f = open(file_path)
            return True
        except IOError as e:
           return False

    def cleanup(self):
        """
        removes all files in the download folder
        """
        for file in os.listdir(self.download_path):
            file_path = os.path.join(self.download_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e
