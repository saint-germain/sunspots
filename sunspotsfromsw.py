# this function returns the sunspot number from the source code of a timestamped url from spaceweather.com
def request(myday,mymonth,myyear):
    import urllib2
# write on top of the url with the mydate info as the timestamp
    url = 'http://spaceweather.com/archive.php?view=1&day=%s&month=%s&year=%s' % (myday,mymonth,myyear)
# get source code from url
    request = urllib2.Request(url)
    handle = urllib2.urlopen(request)
    content = handle.read()
# get string between two given strings
# split page in two: before=[0] and after=[1] a given string
    splitted_page = content.split("<b>Sunspot number:", 1);
# split page after previous string but before new string = desired string
    splitted_page = splitted_page[1].split("</b></span>");
# before 2009.12.25 the page format changes
    if myyear < 2010:
# between 2009.12.25 and 2009.12.31 the format is the same as after 2010.01.01
# this means we don't have to split the page again
        if myyear == 2009 and int(mymonth) == 12 and int(myday) >= 25:
            return int(splitted_page[0])
# before 2009.12.25 the sunspot number is between <font> arguments
        splitted_page=splitted_page[0].split(">", 1);
        splitted_page = splitted_page[1].split("</font>"); 
# return sunspot number
    return int(splitted_page[0])
    
    
from datetime import date
from datetime import datetime
from datetime import timedelta
# open output file
f = open("spots.txt","w")
# set today's time just in case
today=datetime.now()
# user sets start and end dates 
# end date can be set to today
# year month day format
start=datetime(2008,10,06)
end=datetime(2009,02,23)
#end=today
# label dataset file using the start date
f.write("Start date (y/m/d) = %s\n" % (start.date()))
# set number of iterations from the number of days between user-given dates
number=(end-start).days+2
# iterate over date range
# k is our universal index number, I guess it can be translated into Julian Date
for k in range (1,number):
# set the date for the url timestamp
    mydate = start+timedelta(days=k-1)
# format day and month in double digits, e.g. jan 3rd = 01 03 not 1 3
    myday=str('{0:02d}'.format(mydate.day))
    mymonth=str('{0:02d}'.format(mydate.month))
    myyear=mydate.year
# get number of sunspots from above function
    nspots=request(myday, mymonth, myyear)
# label accordingly to which day of the year we're getting, in strict numerical order
# e.g. december 31st = 365 (in a non-leap year)
    yrstart=datetime(mydate.year,01,01)
    numday=(mydate-yrstart).days+1
# write to file year, numerical day, index number, and solar spots number
    print myyear,numday,k,nspots
    f.write("%s %s %s %s\n" % (myyear,numday,k,nspots))
    
f.close()