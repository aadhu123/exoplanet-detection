import urllib.request
import numpy as np
import csv
import re
import os
import os.path
import tarfile

# This SDK does not support all features of the API, but is simply a simple wrapper around
# it to keep your code cleaner.
class MAST:
    __rootUrl = "https://archive.stsci.edu/"
    __baseUrl = ""
    # All avaiables MAST data sets (https://archive.stsci.edu/vo/mast_services.html)
    __dataSets = [
        "hst",
        "hsc_sum",
        "hsc",
        "kepler/data_search",
        "kepler/kepler_fov",
        "kepler/kic10",
        "kepler/kgmatch",
        "kepler/confirmed_planets",
        "kepler/published_planets",
        "kepler/koi",
        "kepler/ffi",
        "k2/epic",
        "k2/data_search",
        "k2/published_planets",
        "k2/ffi",
        "iue",
        "hut",
        "euve",
        "fuse",
        "uit",
        "wuppe",
        "befs",
        "tues",
        "imaps",
        "hlsp",
        "pointings",
        "copernicus",
        "hpol",
        "vlafirst",
        "xmm-om",
        "swift_uvot"
    ]

    def __init__(self, dataSet):
        self.setDataSet(dataSet)
    
    def setDataSet(self, dataSet):
        if (dataSet not in self.__dataSets):
            raise Exception("The data set '%s' is not available, please choose one of "
                            "the following data sets:\n\n%s"%(
                                dataSet, 
                                "\n".join(self.__dataSets)
                            ))
        
        self.__baseUrl = self.__rootUrl + dataSet + "/search.php?outputformat=CSV&action=Search&"
    
    # An open function to search the data sets, not secure, it could be that requests fail
    # if not used properly. See https://archive.stsci.edu/vo/mast_services.html for more
    # information on searches. 
    def search(self, params):
        searchUrl = self.__baseUrl

        if (type(params) is not dict):
            raise Exception("The `params` argument needs has to be of type `dict`")

        for field, value in params.items():
            searchUrl += "{field}={value}&".format(field=field, value=value)

        response = urllib.request.urlopen(searchUrl).read().decode('utf-8')
        return self.parseCSV(response)

    @staticmethod
    def fetchLightCurve(kicId, downloadDir):
        if (type(kicId) is int):
            kicId = str(kicId)
        elif (type(kicId) is not str):
            raise Exception("The KIC ID needs to be of type `str`")

        # KIC ID has 9 digits
        kicId = kicId.zfill(9)
        # See https://archive.stsci.edu/kepler/download_options.html for specs
        url = "https://archive.stsci.edu/pub/kepler/lightcurves/{shortId}/{longId}/".format(shortId = kicId[0:4], longId = kicId)

        response = urllib.request.urlopen(url).read().decode('utf-8')
        fileName = re.search("kplr%s_lc_Q\d+.tar"%kicId, response).group(0)

        downloadPath = os.path.join(downloadDir, fileName)
        print("Tar file downloading to %s..."%downloadPath)
        urllib.request.urlretrieve(url + fileName, downloadPath)
        print("Download complete\nUnpacking...")
        tar = tarfile.open(downloadPath)
        tar.extractall(path=downloadDir)
        tar.close()
        print("Unpacked to %s\nUnlinking tar file..."%os.path.join(downloadDir, kicId))
        os.unlink(downloadPath)
        print("Process completed")
        
    
    def parseCSV(self, CSVString):
        CSVArray = []

        for line in CSVString.splitlines():
            CSVArray.append(line.split(","))
        
        return np.array(CSVArray)

