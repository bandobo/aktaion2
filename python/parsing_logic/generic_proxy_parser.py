import pandas as pd
import re
import urllib


# Define epoch to datetime support method for the line parser
def to_epoch(dt):
    """Take and epoch time and return a pandas date-time object"""
    try:
        # @todo simplify the logic here to remove offsets before we compute
        timestamp_str = str(dt)
        if timestamp_str.find("-08:00"):
            epoch = pd.to_datetime('1970-01-01 00:00:00-08:00')
            return (dt - epoch).total_seconds()
        elif timestamp_str.find("-07:00"):
            epoch = pd.to_datetime('1970-01-01 00:00:00-07:00')
            return (dt - epoch).total_seconds()
        elif timestamp_str.find("-06:00"):
            epoch = pd.to_datetime('1970-01-01 00:00:00-06:00')
            return (dt - epoch).total_seconds()
    except TypeError as e:
        # print some values here to troubleshoot and return 0 values in the case the logic errors out
        print("Timestamp format issue with epoch time arithmetic.")
        print("Input Type, Value: ", print(type(dt), ",", print(str(dt))))

        epoch = pd.to_datetime('1970-01-01 00:00:00-08:00')
        print("Epoch Origin Type, Value: ", print(type(epoch), ",", print(str(epoch))))
        return (epoch - epoch).total_seconds()


#  given a line of a generic log entry of the format shown in line 7, return a dictionary of labeled information
def generic_line_parser(log_line):
    """take a proxy-log formatted log line and return a dictionary with appropriate key names"""
    # example data
    # logLine = '[09/Jan/2014:04:53:04 -0800] "Nico Rosberg" 172.16.2.101 77.75.107.241 1500 200 TCP_HIT "GET http://www.divernet.com/ HTTP/1.1" "Internet Services" "low risk " "text/html; charset=utf-8" 470 396 "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)" "http://www.google.com/url?sa=t&rct=j&q=&esrc=s&frm=1&source=web&cd=1&sqi=2&ved=0CCoQFjAA&url=http%3A%2F%2Fwww.divernet.com%2F&ei=opvOUpyXFrSA2QXnv4DwDg&usg=AFQjCNHeSe4ebK0u69M-TBEGNkTZy-C-Nw&bvm=bv.59026428,d.b2I" "-" "0" "" "-" '
    log_pattern = '\[(?P<dateTime>.*?) (?P<timezone>.*?)\] \"(?P<userName>.*?)\" (?P<origHost>.*?) (?P<respHost>.*?) (?P<unknownValue>.*?) (?P<statusCode>.*?) (?P<cacheResult>.*?) \"(?P<httpMethod>.*?) (?P<fullUrl>.*?) HTTP/(?P<httpVersion>.*?)\" \"(?P<domainClassification>.*?)\" \"(?P<riskClassification>.*?)\" \"(?P<mimeType>.*?)\" (?P<bytesSent>.*?) (?P<bytesReceived>.*?) \"(?P<userAgent>.*?)\" \"(?P<referrer>.*?)\" \"(?P<urlMeta1>.*?)\" \"(?P<urlMeta2>.*?)\" \"(?P<urlMeta3>.*?)\" \"(?P<urlMeta4>.*?)\"'

    try:
        matched = re.match(log_pattern, log_line)
        matched_dict = matched.groupdict()
    except ValueError as e:
        print("Invalid log format, does not match")
        print(log_pattern)
    except AttributeError as e:
        print("Invalid log format, does not match")
        print(log_pattern)

    # get the timestamp as a string, reformatted to feed into pd.to_datetime
    # get the epoch time using the to_epoch function

    val_partitioned = log_line.split(" ")
    dt_string = val_partitioned[0].replace("[", "").replace(":", " ", 1)
    time_zone = val_partitioned[1].replace("]", "")
    # timeZone = timeZone.replace("0","")
    dt_string = dt_string + " " + time_zone

    dt_obj = pd.to_datetime(dt_string)
    epoch_time = to_epoch(dt_obj)

    # now appended the dictionary with the dt_obj object and dt_string and
    # the concatenated URL meta data

    try:
        matched_dict['epochTime'] = epoch_time
        matched_dict['timeString'] = dt_string
        matched_dict['urlMeta'] = matched_dict['urlMeta1'] + " " + matched_dict['urlMeta2'] + " " + matched_dict[
            'urlMeta3'] + " " + matched_dict['urlMeta4']

        # Add uri key/value pair with urllib.parse
        matched_dict['uri'] = urllib.parse.urlparse(matched_dict['fullUrl']).path

        # Add host key/value pair with urllib.parse
        matched_dict['host'] = urllib.parse.urlparse(matched_dict['fullUrl']).netloc

        # Cast epochTime into tslib.timeStamp datatype
        matched_dict['epochTime'] = pd.to_datetime(matched_dict['epochTime'], unit='s')
        return matched_dict

    except UnboundLocalError:
        print("parsing error at log line " + log_line)
        return {}


def generic_proxy_parser(file):
    """Takes a fully-qualified file-path and returns a dataframe of the file contents"""
    # instantiate the local vars
    # df_proxy = pd.DataFrame()
    proxy_ls = []

    # run through the file, calling generic_line_parser for each line.
    with open(file) as f:
        for line in f:
            # get a line
            line = line.rstrip('\n')

            # turn line string into dictionary
            proxy_dic = generic_line_parser(line)
            # print(proxy_dic)

            # append a copy of the dictionary the local list
            proxy_ls.append(proxy_dic.copy())
            # print(proxy_ls)

    # return a dataFrame made from proxy_ls
    return pd.DataFrame(proxy_ls)


def test_generic_line_parser():
    test_line = '[09/Jan/2014:04:53:04 -0800] "Nico Rosberg" 172.16.2.101 77.75.107.241 1500 200 TCP_HIT "GET http://www.divernet.com/ HTTP/1.1" "Internet Services" "low risk " "text/html; charset=utf-8" 470 396 "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)" "http://www.google.com/url?sa=t&rct=j&q=&esrc=s&frm=1&source=web&cd=1&sqi=2&ved=0CCoQFjAA&url=http%3A%2F%2Fwww.divernet.com%2F&ei=opvOUpyXFrSA2QXnv4DwDg&usg=AFQjCNHeSe4ebK0u69M-TBEGNkTZy-C-Nw&bvm=bv.59026428,d.b2I" "-" "0" "" "-"'
    test_dict = {'bytesReceived': '396',
                'bytesSent': '470',
                'cacheResult': 'TCP_HIT',
                'epochTime': 1389271984.0,
                'dateTime': '09/Jan/2014:04:53:04',
                'respHost': '77.75.107.241',
                'domainClassification': 'Internet Services',
                'httpMethod': 'GET',
                'httpVersion': '1.1',
                'mimeType': 'text/html; charset=utf-8',
                'riskClassification': 'low risk ',
                'origHost': '172.16.2.101',
                'statusCode': '200',
                'timeString': '09/Jan/2014 04:53:04 -0800',
                'timezone': '-0800',
                'unknownValue': '1500',
                'urlMeta': '- 0  -',
                'urlMeta1': '-',
                'urlMeta2': '0',
                'urlMeta3': '',
                'urlMeta4': '-',
                'urlRequested': 'http://www.divernet.com/',
                'userAgent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; '
                             'Trident/6.0)',
                'userName': 'Nico Rosberg',
                'referrer': 'http://www.google.com/url?sa=t&rct=j&q=&esrc=s&frm=1&source=web&cd=1&sqi=2&ved=0CCoQFjAA&url=http%3A%2F%2Fwww.divernet.com%2F&ei=opvOUpyXFrSA2QXnv4DwDg&usg=AFQjCNHeSe4ebK0u69M-TBEGNkTZy-C-Nw&bvm=bv.59026428,d.b2I'}
    assert generic_line_parser(test_line) == test_dict

# def test_invalid_log_format_exception():
#     badFormatLine = ' "Nico Rosberg" 77.75.107.241 1500 200 TCP_HIT "GET http://www.divernet.com/ HTTP/1.1" "Internet Services" "low risk " "text/html; charset=utf-8" 470 396 "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)" "http://www.google.com/url?sa=t&rct=j&q=&esrc=s&frm=1&source=web&cd=1&sqi=2&ved=0CCoQFjAA&url=http%3A%2F%2Fwww.divernet.com%2F&ei=opvOUpyXFrSA2QXnv4DwDg&usg=AFQjCNHeSe4ebK0u69M-TBEGNkTZy-C-Nw&bvm=bv.59026428,d.b2I" "-" "0" "" "-" '
#     pytest.raises(AttributeError, generic_line_parser, badFormatLine)
