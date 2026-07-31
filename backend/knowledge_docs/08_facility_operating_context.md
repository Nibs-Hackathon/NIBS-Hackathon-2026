# Facility Operating Context

This directory gives the knowledge retriever a high-level operating context for the RigOS demonstration portfolio. It is not a source of equipment limits, emergency numbers, or regulatory commitments; site-controlled records remain authoritative.

## Americas Portfolio

Texas Gulf Coast operations should account for heat, humidity, hurricanes, salt exposure, and large integrated process-unit dependencies. Alberta North operations add winterization, freeze protection, remote logistics, and cold-start concerns. A Brazil Atlantic site should emphasize tropical rainfall, coastal corrosion, and supply-chain lead time.

## Europe and Africa Portfolio

North Sea operations require attention to marine weather, wind exposure, salt ingress, and constrained offshore or coastal access. Rotterdam-area operations operate within dense industrial and logistics networks where interface management matters. West African coastal operations may need additional planning for humidity, marine corrosion, contractor logistics, and spares availability.

## Middle East and Asia Portfolio

Gulf-region sites should account for high ambient temperature, dust, cooling-system demand, and saline coastal exposure. Singapore-area operations should account for tropical rainfall, lightning, humidity, and dense marine logistics.

## India Portfolio

Mumbai Coastal combines monsoon rain, salt exposure, urban logistics, and high humidity. Jamnagar Energy combines high heat, dust, saline coastal influence, and a large integrated asset base. Paradip Eastern requires cyclone and storm-surge readiness alongside monsoon drainage and coastal corrosion management. Chennai South combines heat, seasonal heavy rain, cyclone exposure, and coastal atmospheric corrosion.

## Near-India Regional Portfolio

Colombo Gateway should plan around monsoon patterns, marine logistics, humidity, and coastal corrosion. Chattogram Bay should account for intense rainfall, cyclone exposure, drainage readiness, and port-interface constraints.

## Facility-Specific Data Separation

Each facility must retain its own asset identifiers, telemetry series, incidents, work orders, health calculations, and reports. Enterprise views may aggregate these records but must preserve the originating facility and asset lineage. Never copy a measurement or decision between facilities merely to fill a missing value.

## Context Selection

When answering a facility question, combine this regional context with the selected facility, current asset state, recent readings, open incidents, and linked evidence. If the facility is not known, state that limitation and answer at portfolio level.

## Operating-Limit Guardrail

Do not infer alarm setpoints, trip values, inspection intervals, chemical limits, or safe operating envelopes from this overview. Retrieve the site-approved operating procedure, equipment manual, inspection plan, or management-of-change record before recommending a numeric threshold.
