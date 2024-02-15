INSERT INTO race_data
( race_id
, type
, position_display_order
, position_number
, position_text
, driver_number
, driver_id
, constructor_id
, engine_manufacturer_id
, tyre_manufacturer_id
, fastest_lap_lap
, fastest_lap_time
, fastest_lap_time_millis
, fastest_lap_gap
, fastest_lap_gap_millis
, fastest_lap_interval
, fastest_lap_interval_millis
)
VALUES
( ?1.id
, ?2.type
, ?2.positionDisplayOrder
, ?3.positionNumber
, ?3.positionText
, ?3.driverNumber
, ?3.driverId
, ?3.constructorId
, ?3.engineManufacturerId
, ?3.tyreManufacturerId
, ?3.lap
, ?3.time
, ?3.timeMillis
, ?3.gap
, ?3.gapMillis
, ?3.interval
, ?3.intervalMillis
);
