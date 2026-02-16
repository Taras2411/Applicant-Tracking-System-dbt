select distinct on (app_id)
    app_id,
    candidate_id,
    role_level,
    applied_date,
    decision_date,

    case 
        when expected_salary < 0 then null 
        else expected_salary 
    end as expected_salary
from {{ source('hr_raw_data', 'raw_applications') }}
where 

    app_id is not null 
    and candidate_id is not null
    and (decision_date is null or decision_date >= applied_date)

order by app_id, applied_date desc