# Handover exercise: build form 17 yourselves

The client asked that, before handover, their own staff build one new process on the framework while the
consultant only advises. Here's a two-hour exercise that proves the framework is reusable.

**New form:** Vehicle booking (process `LOGISTICS`).

1. Add a row to `grt_form`: code `VEH`, release 3, process `LOGISTICS`, numbering `VB-{SEQNUM:5}`, budget check no.
2. Create the detail table `grt_vehiclebooking` (request, vehicle, from, to, destination, driver needed).
3. Add two approval rules: stage 1 `LINE_MANAGER`, stage 2 `LOGISTICS_OFFICER`.
4. Copy the parent flow *GRANT – Parent – Leave*, change the form filter to `VEH`, save.
5. Add a screen to the self-service canvas app (copy the Leave screen).
6. Test with `python scripts/grant_engine.py` after adding a sample request row, then for real in Dev.
7. Deploy with the pipeline.

**Pass criteria:** no change to any child flow, no hard-coded email, no new connection. If they needed to touch
the engine, the engine isn't finished.
