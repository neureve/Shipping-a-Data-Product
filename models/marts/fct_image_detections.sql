{{ config(materialized='table') }}

SELECT
  rid.message_id,
  rid.detected_object_class,
  rid.confidence_score,
  msg.channel,
  msg.date
FROM {{ ref('raw_image_detections') }} AS rid
JOIN {{ ref('fct_messages') }} AS msg
ON rid.message_id = msg.id
