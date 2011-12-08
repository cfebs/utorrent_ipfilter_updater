import gzip
import os
from nose.tools import *
from ipfilter_updater.filter_parser import * 

p2p_lines = ["# this is a comment",
            "\t   Detected AP2P on SaudiNet  :  2.88.46.254-2.88.46.254",
            "s0-0.ciscoseattle.bbnplanet.net  :  4.0.25.146 - 4.0.25.148\n"]

dat_lines = ["# this is a comment",
            "012.045.127.000-012.045.127.255,090,   \t [L1]MERCURY INTERACTIVE",
            "  012.045.128.032-  012.045.128.039, \t 100,  \t [L2]BANKERS LIFE CASUALTY"]

gzip_p2p = 'files/gzip_p2p.gz'
dat = 'files/dat_file.dat'

class TestClass:

    def setup(self):
        f = gzip.open(gzip_p2p, 'wb')
        f.write('\n'.join(p2p_lines))
        f.close()

        f = open(dat, 'wb')
        f.write('\n'.join(dat_lines))
        f.close()

    def teardown(self):
        # cleanup files
        os.remove(gzip_p2p)
        os.remove(dat)
        return

    def test_filter_init(self):
        f = Filter(gzip_p2p)
        assert_not_equal(None, f.file_path)

    def test_is_comment(self):
        f = Filter(gzip_p2p)
        comment = f.is_comment('# this is a comment')
        assert_true(comment)

    def test_not_comment(self):
        f = Filter(gzip_p2p)
        comment = f.is_comment('this is a comment')
        assert_false(comment)


    def test_p2p_init(self):
        f = P2PFilter(gzip_p2p)
        assert_equal(gzip_p2p, f.file_path)

    def test_dat_init(self):
        f = DatFilter(dat)
        assert_equal(dat, f.file_path)

    def test_p2p_to_dat(self):
        p2p = P2PFilter(gzip_p2p)
        dat = p2p.to_dat()
        expected = ['2.88.46.254-2.88.46.254,000,Detected AP2P on SaudiNet',
                    '4.0.25.146-4.0.25.148,000,s0-0.ciscoseattle.bbnplanet.net']
        assert_equals(expected, dat)

    def test_dat_to_p2p(self):
        dat_filter = DatFilter(dat)
        p2p = dat_filter.to_p2p()
        expected = ["[L1]MERCURY INTERACTIVE:012.045.127.000-012.045.127.255",
                    "[L2]BANKERS LIFE CASUALTY:012.045.128.032-012.045.128.039"]

        assert_equals(expected, p2p)
