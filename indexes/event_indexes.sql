-- Author Philip Lane and Claude Sonnet 4.5

-- Date to query events by date
CREATE INDEX IX_Event_Date
ON Event (event_date);

-- Organizer to query events by organizer
CREATE INDEX IX_Event_OrganizerID
ON Event (organizer_id);

-- Location to query events by location
CREATE INDEX IX_Event_LocationID
ON Event (location_id);
