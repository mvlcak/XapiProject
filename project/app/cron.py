from .models import *
import requests,json
def my_cron_job():
	response = requests.get('https://watershedlrs.com/api/organizations/<yourLrsEndpoint>/query/export?type=json',
                            auth=('', ''))
	text = json.loads(response.text)
	for activity in text:
		if not Person.objects.filter(person_name=activity['actor']['name']):
			person=Person(id_lms=activity['actor']['account']['name'],person_name=activity['actor']['name'])
			person.save()
		else: 
			person=Person.objects.get(person_name=activity['actor']['name'])
		act=Activity(person=person,
		actor=activity['actor']['name'],
		verb=activity['verb']['display']['en'],
		object=activity['object']['definition']['name']['en'],
		pub_date=timezone.now(),
		timestamp =activity['timestamp'],
		id_activity=activity['id'])	
		activities=Activity.objects.filter(id_activity=activity['id'])
		if not activities:
		    act.save()