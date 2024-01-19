from apscheduler.schedulers.background import BackgroundScheduler
from .something_update import *
from apscheduler.triggers.interval import IntervalTrigger

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_something, IntervalTrigger(minutes=90))
    scheduler.start()
    scheduler.print_jobs()

def startcpumem():
    scheduler = BackgroundScheduler()
    scheduler.add_job(dimmemorycpu, IntervalTrigger(hours=24))
    scheduler.start()
    scheduler.print_jobs()

def finich():
    scheduler = BackgroundScheduler()
    scheduler.add_job(del_something, IntervalTrigger(weeks=1))
    scheduler.start()
     

#start_date=datetime.now() 
def collect():
    scheduler = BackgroundScheduler()
    scheduler.add_job(dim, IntervalTrigger(minutes=60))
    scheduler.start()
    scheduler.print_jobs()


def ras():
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(reset, IntervalTrigger(weeks=4))
    scheduler.start()
    scheduler.print_jobs()
    
def sharingIN():
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(bh, IntervalTrigger(minutes=70))
    scheduler.start()
    scheduler.print_jobs()

def resetBH():
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(resetsharing, IntervalTrigger(weeks=4))
    scheduler.start()
    scheduler.print_jobs()
#start_date=datetime.now()
def nodal():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fn_fo_fh, IntervalTrigger(days=2))
    scheduler.start()

def dimnodal():
    scheduler = BackgroundScheduler()
    scheduler.add_job(dimfn, IntervalTrigger(minutes=75))
    scheduler.start()
    scheduler.print_jobs()


def resetnodal():
    scheduler = BackgroundScheduler()
    scheduler.add_job(resetFN, IntervalTrigger(weeks=4))
    scheduler.start()
    scheduler.print_jobs()


def delnodal():
    scheduler = BackgroundScheduler()
    scheduler.add_job(del_FN, IntervalTrigger(weeks=111))
    scheduler.start()

def dimsw():
    scheduler = BackgroundScheduler()
    scheduler.add_job(dim_sw, IntervalTrigger(minutes=73))
    scheduler.start()
    scheduler.print_jobs()


def reset_sw():
    scheduler = BackgroundScheduler()
    scheduler.add_job(resetsw, IntervalTrigger(weeks=4))
    scheduler.start()
    scheduler.print_jobs()


def reset_cpu():
    scheduler = BackgroundScheduler()
    scheduler.add_job(resetdimcpu, IntervalTrigger(weeks=4))
    scheduler.start()
    scheduler.print_jobs()


def tOPONODE():
    scheduler = BackgroundScheduler()
    scheduler.add_job(generatenode, IntervalTrigger(weeks=1 ))
    scheduler.start()
    scheduler.print_jobs()
    
def tOPOLink():
    scheduler = BackgroundScheduler()
    scheduler.add_job(generatelink, IntervalTrigger(weeks=1))
    scheduler.start()
    scheduler.print_jobs()


def reporting():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reportingservice, IntervalTrigger(weeks=1))
    scheduler.start()
    scheduler.print_jobs()