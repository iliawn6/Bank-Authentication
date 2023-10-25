from __future__ import absolute_import, unicode_literals
import os 
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Authorization.settings') 
  
app = Celery('Authorization')   
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks()



#print("TESTING")



# app.conf.beat_schedule = {
#     'check-every-10-seconds':{
#         'task': 'data_collection.tasks.consume',
#         'schedule': 10.0,
#     },
# }

# # app.conf.beat_schedule = {
# #     'add-every-30-seconds': {
# #         'task': 'data_collection.tasks.add',
# #         'schedule': 5.0,
# #         'args': (16, 16)
# #     },
# # }
# app.conf.timezone = 'UTC'

# #app.conf.timezone = 'UTC'

# from __future__ import absolute_import, unicode_literals
# import os

# from celery import Celery

# # Set the default Django settings module for the 'celery' program.
# # "sample_app" is name of the root app
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Authorization.settings')

# app = Celery('Authorization')
            
# # Load task modules from all registered Django apps.
# app.autodiscover_tasks()