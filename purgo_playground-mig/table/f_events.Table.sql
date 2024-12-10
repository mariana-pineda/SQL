
CREATE TABLE purgo_playground.f_events (
  date STRING, 
  event_name STRING, 
  event_ts STRING, 
  user_pseudo_id STRING, 
  event_bundle_sequence_id BIGINT, 
  session_id BIGINT, 
  session_number BIGINT, 
  device_browser STRING, 
  device_category STRING, 
  city STRING, 
  country STRING, 
  region STRING, 
  page_title STRING, 
  adcontent STRING, 
  campaign STRING, 
  traffic_source STRING, 
  traffic_medium STRING, 
  referral_path STRING, 
  keyword STRING, 
  session_engaged STRING, 
  content STRING, 
  search_query STRING, 
  form_name STRING, 
  navigation_item_type STRING, 
  navigation_item_name STRING, 
  content_name STRING, 
  engagement_time BIGINT
)
USING delta

