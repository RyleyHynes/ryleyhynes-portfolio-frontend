from datetime import timedelta, datetime
from .models import Plan, Workout
DIST_TEMPLATE={"easy":5.0,"tempo":8.0,"long":16.0,"strength":0.0}
WEEK_PATTERN=["easy","tempo","easy","strength","easy","long","rest"]
def generate_plan(owner, name, start_date, weeks=12):
    if isinstance(start_date,str): start_date=datetime.fromisoformat(start_date).date()
    plan=Plan.objects.create(owner=owner,name=name,start_date=start_date,weeks=weeks)
    d=start_date
    for _ in range(weeks):
        for kind in WEEK_PATTERN:
            if kind=="rest": d += timedelta(days=1); continue
            Workout.objects.create(plan=plan,date=d,kind=kind,distance_km=DIST_TEMPLATE.get(kind,5.0),duration_min=int(DIST_TEMPLATE.get(kind,5.0)*6))
            d += timedelta(days=1)
    return plan
