#author:azadeh
import re
import entropy as en
import pandas as pd


class HTTPMicroBehaviors:

    def isBase64(s):
        """ Define a class method for matching base64 strings"""
        # check that the string has no remainder in %4, check that it only contains valid characters

        try:
            re_check = re.match('^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$', s)
            return re.match('^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$', s)
        except: TypeError
        return False

    def isUrlEncoded(s):
        """Define a class method for matching url encoded strings"""
        # check if the string contains 1/3 or more % characters
        percentCount = 0
        try:
            for c in s:
                if c == '%':
                    percentCount = percentCount +1

            if (percentCount/len(s)) >= (1/3):
                return(True)
            else:
                return(False)
        except(ZeroDivisionError):
            # Catch all exceptions, specifically division by 0 from empty strings
            return(False)

    def max_path_length(inList):
        """return the max path length of all URIs in list"""
        # Declare local var that will store the max path length
        maxLength = 1

        # Count the depth of the file structure for each uri in inList
        for uri in inList:
            try:
                current_count = uri.count('/')

                # Check the current uri path length against the running length
                if uri.count('/') > maxLength:
                    maxLength = current_count
            except: AttributeError

        return(maxLength)

    def min_path_length(inList):
        """return the min path length of all URIs"""
        # Count the depth of the file structure for each uri in inList
        try:
            for uri in inList:
                minLength = uri.count('/')

                # Check the current uri path length against the running length
                if uri.count('/') < minLength:
                    minLength = uri.count('/')

            return minLength

        except: AttributeError
        return 0


    def max_length(inList):
        """Max length of all URIs in list"""
        maxLength = len(inList.head(1))
        previous_len = 0

        for uri in inList:
            try:
                current_len = len(uri)
                if current_len>= previous_len:
                    maxLength = current_len
                previous_len = current_len
            except: AttributeError

        return(maxLength)

    def min_length(inList):
        """Min length of all URIs in list"""

        minLength = len(inList.head(1))
        previous_len = 0

        for uri in inList:
            try:
                current_len = len(uri)
                if current_len <= previous_len:
                    minLength = current_len
                else:
                    minLength = 0
                previous_len = current_len
            except: AttributeError

        return(minLength)

    def max_entropy(inList):
        """returns the maximum shannon entropy of URIs in the list"""
        try:
            maxEntropy = en.shannon_entropy(inList[0])
        except(IndexError,TypeError,KeyError):
            try:
                maxEntropy = en.shannon_entropy(inList)
            except(TypeError):
                maxEntropy = 0.0

        for uri in inList:
            try:
                if maxEntropy <  en.shannon_entropy(uri):
                    maxEntropy = en.shannon_entropy(uri)
            except(IndexError, TypeError, KeyError):
                print()

        return(maxEntropy)

    def min_entropy(inList):
        """Returns the minimum shannon entropy of URIs in the list"""
        try:
            minEntropy = en.shannon_entropy(inList[0])
        except(IndexError,TypeError,KeyError):
            try:
                minEntropy = en.shannon_entropy(inList)
            except(TypeError):
                minEntropy = 0.0

        for uri in inList:
            try:
                if minEntropy > en.shannon_entropy(uri):
                    minEntropy = en.shannon_entropy(uri)
            except(IndexError, TypeError, KeyError):
                print()

        return(minEntropy)

    def base_64_match(inList):
        """Return the number of URI in inList that could be a base64 encoded string"""

        count = 0

        for uri in inList:
            if HTTPMicroBehaviors.isBase64(uri):
                count = count+1

        return(count)

    def percent_encoding_match(inList):
        """Number of URIs with large number of % encoded strings"""
        count = 0
        for uri in inList:
            if HTTPMicroBehaviors.isUrlEncoded(uri):
                count = count + 1

        return(count)

    def uri_distinct(inSeries):
        """expects a list of URI, returns a integer indicating the number of URI's that are unique"""
        # Instantiate the unique strings counter
        inList = inSeries.tolist()
        count = len(inList)

        # Recursively check for the head of the list in the rest of the list
        while len(inList) > 0:

            # If the head of the list matches, decrement the unique strings counter
            if inList[0] in inList[1:]:
                count = count - 1
            del inList[0]

        return(count)

    def url_percent_encoding_match(inList):
        """expects a list of URI, returns a serues contain boolean flags indicating whether the
            URI at that index is percent encoded"""
        matched = []
        for uri in inList:
            try:
                matched.append(HTTPMicroBehaviors.isUrlEncoded(uri))
            except:
                return(matched)

        return(matched)


    def behaviorVector(inFrame):
        """expects a dataFrame, returns a dictionary
        define a dictionary of learning features: uriMaxPathDepth, uriMinPathDepth, uriMaxLength, uriMinLength, uriDistinct,
        uriMaxEntropy, uriMinEntropy, isBase64, isUrlEncoded"""

        inList = inFrame['uri']

        # Dirty work around for IndexError anomaly generated when calling entropy inside  the dictionary key/value declaration below
        mxEntropy = HTTPMicroBehaviors.max_entropy(inList)
        mnEntropy = HTTPMicroBehaviors.min_entropy(inList)

        behaviorVector = {'max_path_depth': HTTPMicroBehaviors.max_path_length(inList) +
                                            HTTPMicroBehaviors.min_path_length(inList) ,
                          'min_path_depth': HTTPMicroBehaviors.min_path_length(inList) +
                                            HTTPMicroBehaviors.max_path_length(inList),
                          'max_length':     HTTPMicroBehaviors.max_length(inList) +
                                            HTTPMicroBehaviors.min_length(inList),
                          'min_length':     HTTPMicroBehaviors.min_length(inList) +
                                            HTTPMicroBehaviors.max_length(inList),
                          'uri_Distinct':   HTTPMicroBehaviors.uri_distinct(inList),
                          'max_entropy':    mxEntropy + mnEntropy,
                          'min_entropy':    mnEntropy + mxEntropy,
                          'base64Match':    HTTPMicroBehaviors.base_64_match(inList),
                          'percentEncoded': HTTPMicroBehaviors.url_percent_encoding_match(inList)}

        timing_vector = TimeBehaviors.behavior_vector(inFrame)

        uri_dict = dict(behaviorVector)
        uri_dict.update(timing_vector)
        return(uri_dict)


class TimeBehaviors:


    """Class specific method for calculating difference between time-stamps,
        expects list of date timese, type float"""
    def time_delta(times):
        delta = times[1]-times[0]
        return(delta.total_seconds())

    def get_time_interval(inFrame):
        """List of time-deltas from first to last,
        expects a dataFrame, returns a list of seconds in float format"""
        #declare list that will hold deltas
        deltas = []
        #cast inFrame epochTime column into a list
        times = inFrame['epochTime'].tolist()

        #read through the epochTime list until empty
        while len(times) > 1:
            #for each iteration, calculate the total second time delta
            deltas.append(TimeBehaviors.time_delta(times))
            #strip the head off the list
            times.remove(times[0])
        #return the list of time deltas
        return(deltas)

    def max_time_interval(inFrame):
        """Returns the maximum time interval in a window,
            expects a dataFrame, returns a float"""
        return(max(TimeBehaviors.get_time_interval(inFrame)))

    def min_time_interval(inFrame):
        """Returns the minimum time interval in a window
            expects a dataFrame, returns a float"""
        return(min(TimeBehaviors.get_time_interval(inFrame)))

    def interval_length(inFrame):
        """Time Length in Window,
            expects a dataFrame, returns window time delta, difference of last and first time stamps"""
        #last row number of the inFrame
        d0 = TimeBehaviors.min_time_interval(inFrame)
        d1 = TimeBehaviors.max_time_interval(inFrame)
        return(d1-d0)

    def get_max_deltas(inFrame, n=5):
        """Get a list containing the max deltas info, default is top 5
            expects a dataFrame, returns a list of floats"""
        #get time deltas list
        DeltasList = TimeBehaviors.get_time_interval(inFrame)

        #sort DeltasList
        DeltasList = sorted(DeltasList, reverse=True)

        #return size
        return_size = n
        if n == 0:
            return(DeltasList[:5])
        else:
            return(DeltasList[:return_size])


    def get_min_deltas(inFrame, n = 5):
        """Get a list containing the min deltas info, default is least 5
            expects a dataFrame, returns a list of floats"""
        #get time deltas list
        DeltasList = TimeBehaviors.get_time_interval(inFrame)

        #sort DeltasList
        DeltasList = sorted(DeltasList)

        #return size
        return_size = n
        if n == 0:
            return(DeltasList[:5])
        else:
            return(DeltasList[:return_size])

    # Group of time-delta ratio counters
    def ratio_of_deltas_A(inFrame):
        """(Ratio of time-deltas < 1 second) / (window size)
            expects a dataFrame, returns a float"""
        counter = 0
        index = 0

        for i in TimeBehaviors.get_time_interval(inFrame):
            if i <= 1:
                counter = counter + 1
        try:
            return(counter / TimeBehaviors.interval_length(inFrame))
        except: ZeroDivisionError

        return 0.0

    def ratio_of_deltas_B(inFrame):
        """(Ratio of time-deltas < 5 second)/(window size)
           expects a dataFrame, returns a float"""
        counter = 0

        for i in TimeBehaviors.get_time_interval(inFrame):
            if i < 5:
                counter = counter + 1
        try:
            return(counter / TimeBehaviors.interval_length(inFrame))
        except: ZeroDivisionError

        return 0.0

    def ratio_of_deltas_C(inFrame):
        """(Ratio of time-deltas < 10 second)/(window size)
            expects a dataFrame, returns a float"""
        counter = 0

        for i in TimeBehaviors.get_time_interval(inFrame):
            if i < 10:
                counter = counter + 1
        try:
            return(counter / TimeBehaviors.interval_length(inFrame))
        except: ZeroDivisionError

        return 0.0

    def ratio_of_deltas_D(inFrame):
        """(Ratio of time-deltas < 20 second)/(window size)
            expects a dataFrame, returns a float"""
        counter = 0

        for i in TimeBehaviors.get_time_interval(inFrame):
            if i < 20:
                counter = counter + 1
        try:
            return(counter / TimeBehaviors.interval_length(inFrame))
        except: ZeroDivisionError

        return 0.0

    def ratio_of_deltas_E(inFrame):
        """(Ratio of time-deltas >= 100 second)/(window size)
            expects a dataFrame, returns a float"""
        counter = 0

        for i in TimeBehaviors.get_time_interval(inFrame):
            if i >= 100:
                counter = counter + 1

        try:
            return(counter / TimeBehaviors.interval_length(inFrame))
        except: ZeroDivisionError

        return 0.0

    def check_if_shortened_url(inList):
        # checks if any shortened Urls are detected
        words = ['bit.ly', 'goo.gl', 'tinylord.com', 'sk.gy', 'short2.in', 't.co', 'adbooth.net', 'adfoc.us', 'bc.vc',
                 'j.gs', 'cutt.us', 'tiny.cc', 'adfa.st', 'ity.im', 'budurl.com', 'soo.gd', 'prettylinkpro.com',
                 'shrinkonce.com', 'ad7.biz', '2tag.nl', '1o2.ir', 'hotshorturl.com', 'onelink.ir', 'dai3.net',
                 '9en.us', 'kaaf.com', 'rlu.ru', 'awe.sm', '4ks.net', 's2r.co', '4u2bn.com','multiurl.com','tab.bz',
                 'dstats.net','iiiii.in','nicbit.com','l1nks.org','at5.us','bizz.cc','fur.ly','clicky.me',''
                 'magiclinker.com','miniurl.com','bit.do','adurl.biz','omani.ac','1y.it','1click.im','1dl.us','4zip.in',
                 'ad4.us','adfro.gs','adnid.com','adshor.tk','adspl.us','adzip.us','articleshrine.com','asso.in',
                 'b2s.me','bih.me','bih.cc','biturl.net','buraga.org','cc.cr','cf6.co','dollarfalls.info',
                 'domainonair.com','gooplu.com','hide4.me','ik.my','ilikear.ch','infovak.com','its.bz',
                 'jetzt-hier-klicken.de','kly.so','lst.bz','mrte.ch','multiurlscript.com','nowlinks.net','nsyed.com',
                 'ooze.us','ozn.st','scriptzon.com','short2.in','shortxlink.com','shr.tn','shrt.in','sitereview.me',
                 'sk.gy','snpurl.biz','socialcampaign.com','swyze.com','theminiurl.com','tinylord.com','tinyurl.ms',
                 'tip.pe','ty.by']

        for word in words:
            if word in inList:
                return True
            else:
                return False

    def RiskyExtention(inList):
        from urllib.parse import urlparse
        o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')
        o.scheme
        o.port
        print(o)
        currentpath = o.path
        # splitpath=currentpath.split(".")
        testlist = ['.pdf', '.exe', '.mp3', '.mp4', '.bin', '.zip', '.gif', '.jpg', '.ps1', '.bat', '.bin',
                    '.ps', '.jar', '.txt', '.rar', '.avi', '.mov', '.avi']
        lastpath = currentpath[:-4]

        if lastpath in testlist:
            return True
        else:
            return False

    def behavior_vector(self, n = 5):
        """Given a dataFrame with time-ordered lists as entries:
                    return dictionary with entries get_time_interval, get_max_deltas, get_min_deltas
                     time_delta, ratio_of_deltas_A,  ratio_of_deltas_B,  ratio_of_deltas_C,
                      ratio_of_deltas_D,  ratio_of_deltas_E, max_time_interval, min_time_interval
                      interval_length"""

        #define the behavior Vector
        behaviorVector = {'time_interval':     TimeBehaviors.get_time_interval(self),
                          'max_deltas':        TimeBehaviors.get_max_deltas(self) +
                                               TimeBehaviors.get_min_deltas(self),
                          'min_deltas':        TimeBehaviors.get_min_deltas(self) +
                                               TimeBehaviors.get_max_deltas(self),
                          'ratio_of_deltas_A': TimeBehaviors.ratio_of_deltas_A(self) +
                                               TimeBehaviors.ratio_of_deltas_B(self),
                          'ratio_of_deltas_B': TimeBehaviors.ratio_of_deltas_B(self) +
                                               TimeBehaviors.ratio_of_deltas_A(self),
                          'ratio_of_deltas_C': TimeBehaviors.ratio_of_deltas_C(self) +
                                               TimeBehaviors.ratio_of_deltas_D(self),
                          'ratio_of_deltas_D': TimeBehaviors.ratio_of_deltas_D(self) +
                                               TimeBehaviors.ratio_of_deltas_E(self),
                          'ratio_of_deltas_E': TimeBehaviors.ratio_of_deltas_E(self) +
                                               TimeBehaviors.ratio_of_deltas_C(self),
                          'max_time_interval': TimeBehaviors.max_time_interval(self) +
                                               TimeBehaviors.min_time_interval(self),
                          'min_time_interval': TimeBehaviors.min_time_interval(self) +
                                               TimeBehaviors.max_time_interval(self),
                          'interval_length':   TimeBehaviors.interval_length(self) +
                                               TimeBehaviors.min_time_interval(self) +
                                               TimeBehaviors.max_time_interval(self),
                          'short_url':         TimeBehaviors.check_if_shortened_url(self),
                          'risk_extention' :   TimeBehaviors.RiskyExtention(self)}
        return(behaviorVector)

