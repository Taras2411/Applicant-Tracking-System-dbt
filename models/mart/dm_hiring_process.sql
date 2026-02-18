{{ config(
    materialized='table'
) }}

with applications as (
    select * from {{ ref('int_ats__applications_joined') }}
),

candidates as (
    select * from {{ ref('stg_ats__candidates') }}
),

-- Агрегируем только успешные интервью
passed_interviews as (
    select 
        app_id,
        count(interview_id) as total_passed_interviews
    from {{ ref('int_ats__interviews_validated') }}
    where outcome = 'Passed'
    group by 1
)

select
    a.app_id,
    c.full_name as candidate_name,
    c.source as candidate_source,
    a.role_level,
    a.applied_date,
    a.decision_date,
    -- Расчет Time-to-Decision (Время до принятия решения в днях)
    date_diff('day', a.applied_date, a.decision_date) as time_to_decision,
    coalesce(p.total_passed_interviews, 0) as total_passed_interviews,
from applications a
left join candidates c on a.candidate_id = c.candidate_id
left join passed_interviews p on a.app_id = p.app_id