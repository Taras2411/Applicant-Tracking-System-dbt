select distinct on (interview_id)
    interview_id,
    app_id,
    interview_date,
    outcome
from {{ source('hr_raw_data', 'raw_interviews') }}
where 
    interview_id is not null
    and app_id is not null
order by interview_id, interview_date desc