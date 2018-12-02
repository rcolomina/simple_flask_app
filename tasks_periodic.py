from celery import Celery
from celery.schedules import crontab
import random_contact as rc

celery_app = Celery("tasks_periodic",
                    broker="redis://127.0.0.1:6379/0") 
# Use local time
celery_app.conf.enable_utc = False

# Import flask app
import Flask as flask
app_flask = flask.app.test_client()
with flask.app.app_context():
    flask.setup() 

celery_app.conf.beat_schedule = {
    "post-contact":{
        "task":"tasks_periodic.post_random_contact",
        "schedule": 15.0
    }
    ,
    "delete-contact":{
         "task":"tasks_periodic.delete_older_entries",
         "schedule": 15.0
    }    
}


@celery_app.task
def post_random_contact():

    # Post a new randowm contact
    random_contact_json = rc.get_random_contact_json()    
    rv = app_flask.post('/contact/',json=random_contact_json)    
    return rv

@celery_app.task
def delete_older_entries():

    # Select all usernames
    rv = app_flask.get('/contact/')
    json_data = rv.get_json()
    print(json_data)

    if json_data['status'] == 200:
        import datetime
        import time
        timeStampNow  = time.mktime(datetime.datetime.utcnow().timetuple())
        
        usersToDelete = [x["username"] for x in json_data["contacts"] if x["creationDateTime"] < (timeStampNow - 60)]
        for username in usersToDelete:
            try:
                rv = app_flask.delete('/contact/'+username)
            except:
                return rv
                
        
        print("Users to delete olders than one minute ",usersToDelete)

    return rv

