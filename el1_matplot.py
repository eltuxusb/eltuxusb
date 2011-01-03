import datetime
from pylab import *
date1 = datetime.date( 1952, 1, 1 )
date2 = datetime.date( 2004, 4, 12 )
delta = datetime.timedelta(days=100)
dates = drange(date1, date2, delta)
s1 = rand(len(dates))
plot_date(dates, s1,'r.')
hold(True)
s2 = rand(len(dates))
plot_date(dates, s2,'bo')
legend(('s1','s2'))
