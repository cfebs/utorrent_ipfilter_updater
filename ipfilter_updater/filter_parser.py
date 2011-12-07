import gzip
import re

class Filter(object):
    """ generic functions for different types of filters """

    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None

    def strip_whitespace(self, string):
        """ strips \\t \\n \\r ' ' """
        return string.strip(' \t\n\r')

    def is_comment(self, string):
        """ is a string a comment """
        pattern = '\s*#.*'
        matches = re.search(pattern, string)
        return bool(matches)

class P2PFilter(Filter):
    """
    A filter in the p2p format
    Localhost:127.0.0.1-127.0.0.1
    """
    def __init__(self, file_path):
        super(P2PFilter, self).__init__(file_path)

    def to_dat(self):
        """
        converts from p2p to dat
        returns list of lines
        """
        self.file = gzip.open(self.file_path)
        dat_lines = [] 
        for line in self.file:
            # if a comment, skip
            if (self.is_comment(line)):
                continue

            ip_pat = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            pattern = '(.*):\s*(%s)\s*-\s*(%s)\s*' % (ip_pat, ip_pat)

            matches = re.search(pattern, line)
            comment = self.strip_whitespace(matches.group(1))
            ip1     = self.strip_whitespace(matches.group(2))
            ip2     = self.strip_whitespace(matches.group(3))

            dat_string = "%s-%s,000,%s" %  (ip1, ip2, comment)
            dat_lines.append(dat_string)

        self.file.close()
        return dat_lines

class DatFilter(Filter):
    """
    A filter in the dat format
    DAT format: "000.000.000.000 - 000.255.255.255 , 000 , invalid ip"
    """
    def __init__(self, file_path):
        super(DatFilter, self).__init__(file_path)

    def to_p2p(self):
        self.file = open(self.file_path)
        dat_lines = [] 
        for line in self.file:
            if (self.is_comment(line)):
                continue

            ip_pat = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            pattern = '^\s*(%s)\s*-\s*(%s)\s*\,\s*\d{1,3}\s*\,(.*)' % (ip_pat, ip_pat)
            

            matches = re.search(pattern, line)
            ip1     = self.strip_whitespace(matches.group(1))
            ip2     = self.strip_whitespace(matches.group(2))
            description = self.strip_whitespace(matches.group(3))
            
            dat_string = "%s:%s-%s" %  (description, ip1, ip2)
            dat_lines.append(dat_string)

        self.file.close()
        return dat_lines
