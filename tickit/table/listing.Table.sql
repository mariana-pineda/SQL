
CREATE TABLE tickit.listing (
	listid INTEGER NOT NULL, 
	sellerid INTEGER NOT NULL, 
	eventid INTEGER NOT NULL, 
	dateid SMALLINT NOT NULL, 
	numtickets SMALLINT NOT NULL, 
	priceperticket NUMERIC(8, 2), 
	totalprice NUMERIC(8, 2), 
	listtime TIMESTAMP WITHOUT TIME ZONE
) DISTSTYLE KEY DISTKEY (listid) SORTKEY (dateid)

