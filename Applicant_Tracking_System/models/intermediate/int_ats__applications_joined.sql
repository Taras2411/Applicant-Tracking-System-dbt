with applications as (
    select * from {{ ref('stg_ats__applications') }}
),

candidates as (
    select * from {{ ref('stg_ats__candidates') }}
)

select
    a.app_id,
    a.candidate_id,
    c.full_name as candidate_name,
    c.source as candidate_source,
    a.role_level,
    a.applied_date,
    a.decision_date
from applications a
inner join candidates c on a.candidate_id = c.candidate_id