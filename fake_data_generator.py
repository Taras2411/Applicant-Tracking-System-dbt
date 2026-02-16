import pandas as pd
import random
import numpy as np
from faker import Faker
from datetime import timedelta, date

fake = Faker()
Faker.seed(42)
random.seed(42)

# Constants
NUM_CANDIDATES = 200
NUM_APPLICATIONS = 250
NUM_INTERVIEWS = 600

def generate_messy_data():
    
    # raw_candidates
    candidates = []
    candidate_ids = list(range(1, NUM_CANDIDATES + 1))
    
    for cid in candidate_ids:
        candidates.append({
            "candidate_id": cid,
            "full_name": fake.name(),
            "source": random.choice(['LinkedIn', 'Referral', 'Career Page', 'Agency']),
            "profile_created_date": fake.date_between(start_date='-2y', end_date='-1y')
        })
    
    df_candidates = pd.DataFrame(candidates)
    
    # raw_applications
    applications = []
    app_ids = list(range(1, NUM_APPLICATIONS + 1))
    
    for aid in app_ids:
        cand = df_candidates.sample(1).iloc[0]
        profile_date = cand["profile_created_date"]
        
        applied_date = fake.date_between(start_date=profile_date, end_date='today')
        
        decision_date = None
        if random.choice([True, True, False]):
            decision_date = applied_date + timedelta(days=random.randint(1, 60))
            if decision_date > date.today():
                decision_date = date.today()
        
        role = random.choice(['Junior', 'Senior', 'Executive'])
        salary = random.randint(40000, 160000)
        
        applications.append({
            "app_id": aid,
            "candidate_id": cand["candidate_id"],
            "role_level": role,
            "applied_date": applied_date,
            "decision_date": decision_date,
            "expected_salary": salary
        })
        
    df_applications = pd.DataFrame(applications)

    #raw_interviews
    interviews = []
    interview_ids = list(range(1, NUM_INTERVIEWS + 1))
    
    for iid in interview_ids:
        app = df_applications.sample(1).iloc[0]
        
        end_date_limit = app["decision_date"] if app["decision_date"] else date.today()
        if end_date_limit <= app["applied_date"]:
            interview_date = app["applied_date"]
        else:
            interview_date = fake.date_between(start_date=app["applied_date"], end_date=end_date_limit)

        interviews.append({
            "interview_id": iid,
            "app_id": app["app_id"],
            "interview_date": interview_date,
            "outcome": random.choice(['Passed', 'Rejected', 'No Show'])
        })
        
    df_interviews = pd.DataFrame(interviews)


    # DATA CORRUPTION
    # 1. Duplicates
    duplicates = df_candidates.sample(n=5)
    df_candidates = pd.concat([df_candidates, duplicates], ignore_index=True)
    
    # 2. Timeliness Violations
    bad_interview_indices = df_interviews.sample(10).index
    for idx in bad_interview_indices:
        app_id = df_interviews.loc[idx, 'app_id']
        app_date = df_applications[df_applications['app_id'] == app_id].iloc[0]['applied_date']
        df_interviews.loc[idx, 'interview_date'] = app_date - timedelta(days=random.randint(10, 30))

    bad_app_indices = df_applications[df_applications['decision_date'].notnull()].sample(5).index
    for idx in bad_app_indices:
        df_applications.loc[idx, 'decision_date'] = df_applications.loc[idx, 'applied_date'] - timedelta(days=5)

    # 3. Orphan Records / FK Violation
    ghost_app = df_applications.iloc[0].copy()
    ghost_app['app_id'] = 9999  
    ghost_app['candidate_id'] = 99999
    df_applications = pd.concat([df_applications, pd.DataFrame([ghost_app])], ignore_index=True)

    # Dirty Data
    # 'LinkedIn' -> 'linkedin', 'Referral' -> ' referral '
    dirty_indices = df_candidates.sample(8).index
    df_candidates.loc[dirty_indices, 'source'] = df_candidates.loc[dirty_indices, 'source'].apply(
        lambda x: x.lower() if random.random() > 0.5 else f" {x} "
    )
    
    neg_salary_idx = df_applications.sample(3).index
    df_applications.loc[neg_salary_idx, 'expected_salary'] = -50000
    
    df_candidates.loc[df_candidates.sample(2).index, 'full_name'] = None

    df_candidates.to_csv('raw_candidates.csv', index=False)
    df_applications.to_csv('raw_applications.csv', index=False)
    df_interviews.to_csv('raw_interviews.csv', index=False)
    
    print("Done!")

if __name__ == "__main__":
    generate_messy_data()