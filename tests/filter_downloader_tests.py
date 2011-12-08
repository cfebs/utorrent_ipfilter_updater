import os
from nose.tools import *
from ipfilter_updater.filter_downloader import * 

test_url = "http://list.iblocklist.com/?list=bt_level1&fileformat=p2p&archiveformat=gz"
test_download_dir = 'files/test_downloads'

class TestClass:
    
    def setup(self):
        return

    def teardown(self):
        # cleanup files
        for file in os.listdir(test_download_dir):
            file_path = os.path.join(test_download_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e

        return

    def test_init(self):
        fd = FilterDownloader([], test_download_dir) 
        assert_equal(test_download_dir, fd.download_path)


    def test_download_file(self):
        fd = FilterDownloader([], test_download_dir) 
        try:
            fd.download_file(test_url)
        except URLError as e:
            print "invalid URL"
            return

        test_path = os.path.join(test_download_dir, 'bt_level1.gz')
        assert_equals([test_path], fd.file_queue)
        assert_true(os.path.isfile(test_path))

    def test_file_exists(self):
        fd = FilterDownloader([], test_download_dir) 
        file_path = os.path.join(test_download_dir, 'test.txt')
        f = open(file_path, 'wb')
        assert_true(fd.file_exists(file_path))
        os.unlink(file_path)
        assert_false(fd.file_exists(file_path))

    def test_cleanup(self):
        fd = FilterDownloader([], test_download_dir) 
        for i in range(0, 5):
            f = open(os.path.join(test_download_dir, ("%d.txt" % i)), 'wb')
            test = "test %d" % i
            f.write(test)
            f.close()

        filecount = 0

        for file in os.listdir(test_download_dir):
            filecount = filecount + 1

        assert_equal(5, filecount)

        fd.cleanup()

        filecount = 0

        for file in os.listdir(test_download_dir):
            filecount = filecount + 1

        assert_equal(0, filecount)
