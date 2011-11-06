import pycurl
import StringIO
import urllib
import md5
from xml.dom.minidom import parseString

''' checkCreditsPost is used to check the remaining credits avaliable in your account using the post method. You must provide your account info, login and password, and it returns the number of credits or -1 if something went wrong  '''
def checkCreditsPost(account, password):
    # The autentification must be done using md5 hash algorithm, so the first thing we be is to code our password
    coded_pass = md5.new()
    coded_pass.update(password)
    coded_pass_str = coded_pass.hexdigest()
    
    # We generate a curl object, which makes a post call to Mensamatic API
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "http://www.mediamovil.es/websiteSMS/sms.asmx/obtenerlimiteSMS")
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.POST, 1)
    data = {'cuenta':account, 'password':coded_pass_str}
    post = urllib.urlencode(data)
    c.setopt(pycurl.POSTFIELDS, post)
    c.perform()
    
    # Now we just have to process the xml returned by Mensamatic API
    dom = parseString(b.getvalue())
    doubleList = dom.getElementsByTagName("double")
    for double in doubleList:
        if double.childNodes[0].nodeValue == '-1':
            return -1
        else:
            return int(double.childNodes[0].nodeValue)
