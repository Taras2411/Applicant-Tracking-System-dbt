{{ config(
    materialized='table'
) }}

with source as (
    select 
        app_id,
        applied_date,
        coalesce(decision_date, current_date) as end_date
    from {{ ref('dm_hiring_process') }}
),

expanded_months as (
    select
        app_id,
        unnest(generate_series(
            date_trunc('month', applied_date), 
            date_trunc('month', end_date), 
            interval 1 month
        )) as report_month
    from source
)

select
    report_month,
    count(distinct app_id) as active_applications
from expanded_months
group by report_month
order by report_month desc