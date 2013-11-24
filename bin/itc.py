#!/usr/bin/python

# This is a wrapper for Apple's java itunes connect report ingestion tool
# (Autoingestion.class). It will download any reports that should be available
# and store them in thex archive directory. It won't download any reports
# that have already been downloaded.

# base
# - archive
#   - daily
#   - weekly
#   - monthly
#   - yearly
# - bin
#   - itc.py
# - conf
#   - autoingestion.properties
# - java
#   - Autoingestion.class

import datetime
import os
import shutil
import subprocess
import sys

BASEDIR = os.getcwd()

# Set this to your vendor id
VENDOR_ID = 00000001

# Set this to the first day of sales
START_DATE = 20130101

def daily_report_dates(start_date):
    """ Get the 30 previous days """
    days = []
    yesterday = datetime.date.today() - datetime.timedelta(1)
    for i in range(0,30):
        d = yesterday - datetime.timedelta(i)
        days.append(int(d.strftime("%Y%m%d")))
    return [d for d in days if d > start_date]

def weekly_report_dates(start_date):
    """ Get the 26 previous weeks """
    days = []
    yesterday = datetime.date.today() - datetime.timedelta(1)
    if yesterday.weekday() == 6:
        sunday = yesterday
    else:
        sunday = yesterday - datetime.timedelta(yesterday.weekday() + 1)
    for i in range(0,26):
        d = sunday - datetime.timedelta(weeks=i)
        days.append(int(d.strftime("%Y%m%d")))
    return [d for d in days if d > start_date]


def monthly_report_dates(start_date):
    """ Get the 12 previous months """
    months = []
    today = datetime.date.today()
    for i in range(1,13):
        if today.month <= i:
            d = today.replace(year=(today.year - 1), month=(today.month + 12 -i))
        else:
            d = today.replace(month=(today.month - i))
        months.append(int(d.strftime("%Y%m")))
    return [m for m in months if m >= (start_date // 100)]

def report_exists(date_type, date):
    valid_date_types = ('Daily', 'Weekly', 'Monthly', 'Yearly')
    if not date_type in valid_date_types:
        raise Exception('Invalid date type')

    filename = 'S_%s_%s_%s.txt.gz' % (date_type[0], str(VENDOR_ID), str(date))
    path = os.path.join(BASEDIR, 'archive', date_type.lower(), filename)

    return os.path.exists(path)


def download_sales_report(date_type, date):
    valid_date_types = ('Daily', 'Weekly', 'Monthly', 'Yearly')
    if not date_type in valid_date_types:
        raise Exception('Invalid date type')

    os.chdir(os.path.join(BASEDIR,'depot'))

    try:
        # First clean out the depot
        for f in os.listdir('.'):
            print >>sys.stderr, "Removing stale depot file %s" % f
            os.remove(f)

        # Run the autoingestion thing. Try not to make too many assumptions
        # about what it might or might not do.
        p = subprocess.Popen(['java', 'Autoingestion', '../conf/autoingestion.properties', str(VENDOR_ID), 'Sales', date_type, 'Summary', str(date)],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]

        # Let's see what it got
        expected_filename = 'S_%s_%s_%s.txt.gz' % (date_type[0], str(VENDOR_ID), str(date))

        files = os.listdir('.')
    
        if len(files) == 0:
            if output == 'There are no reports available to download for this selection.\n':
                # No downloads or updates or anything. Synthesize empty file.
                print >>sys.stderr, "Synthesizing empty report"
                report = 'S_%s_%s_%s.txt' % (date_type[0], str(VENDOR_ID), str(date))
                open(report, 'w').close()
                subprocess.call(['gzip', report])
                files = os.listdir('.')
            else:
                print >>sys.stderr, "No files downloaded."
                print >>sys.stderr, "Autoingest output:"
                print >>sys.stderr, '"%s"' % output

        for f in files:
            if f == expected_filename:
                shutil.copy(f, os.path.join(BASEDIR, 'archive', date_type.lower()))
            else:
                print >>sys.stderr, "Expected %s, got file %s" % (expected_filename, f)
        
        # Clean everything out when we're done
        for f in os.listdir('.'):
            os.remove(f)

    except:
        os.chdir(BASEDIR)
        raise

def main():

    # Initialization
    os.chdir(BASEDIR)
    os.environ['CLASSPATH'] = os.path.join(BASEDIR,'java')

    for d in monthly_report_dates(START_DATE):
        if not report_exists('Monthly', d):
            print "Getting monthly report %s" % str(d)
            download_sales_report('Monthly', d)

    for d in weekly_report_dates(START_DATE):
        if not report_exists('Weekly', d):
            print "Getting weekly report %s" % str(d)
            download_sales_report('Weekly', d)

    for d in daily_report_dates(START_DATE):
        if not report_exists('Daily', d):
            print "Getting daily report %s" % str(d)
            download_sales_report('Daily', d)

main()
