select distinct on (candidate_id)
    candidate_id,
    full_name,
    upper(substr(trim(source), 1, 1)) || lower(substr(trim(source), 2)) as source,
    profile_created_date
from {{ source('hr_raw_data', 'raw_candidates') }}
where candidate_id is not null
order by candidate_id, profile_created_date desc