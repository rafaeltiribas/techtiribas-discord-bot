from croniter import croniter
from datetime import datetime

def get_datetime(cron_exp: str) -> datetime:
	base_time = datetime.now()
	
	cron = croniter(cron_exp, base_time)
	next_execution_time = cron.get_next(datetime)
	
	return next_execution_time