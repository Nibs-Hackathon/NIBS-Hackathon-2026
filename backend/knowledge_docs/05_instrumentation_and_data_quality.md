# Instrumentation, Telemetry, and Data Quality

## Instrument validation

Validate tag identity, engineering unit, range, timestamp, scan quality, calibration status, maintenance state, and whether the value is measured, calculated, substituted, or simulated. Compare redundant instruments and mass or energy balance where available.

## Fault patterns

A flat line may indicate a stable process, a frozen signal, communication failure, or substitution. A single-point spike may be electrical noise or a real fast transient. Drift may result from sensor aging, impulse-line problems, coating, reference-junction issues, density changes, or process change. Contradictory readings require investigation rather than automatic averaging.

## Historian use

Trend enough pre-event and post-event data to establish baseline, onset, rate of change, correlated tags, operator actions, and recovery. Preserve original timestamps and units. Downsampling must not erase short safety-relevant excursions.

## Derived health and forecasts

Health scores and projections are decision-support outputs. Publish the method, data window, freshness, uncertainty, and unavailable state. Do not show invented thresholds or forecasts when the required source data is absent.

## Cyber and control boundaries

Analytics and AI services should be read-only unless a separately approved control path exists. Operator decisions recorded in RigOS are audit records; they must not directly actuate field equipment. Maintain network segmentation, account control, logging, and approved change management.

