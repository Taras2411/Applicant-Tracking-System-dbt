{{ config(
    materialized='table'
) }}

with applications as (
    select * from {{ ref('int_ats__applications_joined') }}
),


valid_hires as (
    select
        candidate_source as source,

        date_trunc('month', decision_date) as hire_month,
        count(app_id) as hires_count
    from applications
    where 
        decision_date is not null

        and date_diff('day', applied_date, decision_date) < 90
    group by 1, 2
),


final as (
    select
        source,
        hire_month,
        hires_count as monthly_hires,
        sum(hires_count) over (
            partition by source 
            order by hire_month
            rows between unbounded preceding and current row
        ) as cumulative_hires
    from valid_hires
)

select * from final
order by source, hire_month