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
    -- Можно сразу протащить дату подачи, если пригодится
    a.applied_date
from interviews i
inner join applications a
    on i.app_id = a.app_id
where 
    -- 1. Проверяем, что интервью было ПОСЛЕ или В ДЕНЬ подачи
    i.interview_date >= a.applied_date
    -- 2. Если нужны только интервью с существующей заявкой, INNER JOIN это уже сделал