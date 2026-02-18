with interviews as (
    select * from {{ ref('stg_ats__interviews') }}
),

applications as (
    select * from {{ ref('stg_ats__applications') }}
)

select
    i.interview_id,
    i.app_id,
    i.interview_date,
    i.outcome,
    a.applied_date
from interviews i
inner join applications a
    on i.app_id = a.app_id
where 
    i.interview_date >= a.applied_date