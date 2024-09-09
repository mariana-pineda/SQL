
CREATE TABLE tickit.sales (
	salesid INTEGER NOT NULL, 
	listid INTEGER NOT NULL, 
	sellerid INTEGER NOT NULL, 
	buyerid INTEGER NOT NULL, 
	eventid INTEGER NOT NULL, 
	dateid SMALLINT NOT NULL, 
	qtysold SMALLINT NOT NULL, 
	pricepaid NUMERIC(8, 2), 
	commission NUMERIC(8, 2), 
	saletime TIMESTAMP WITHOUT TIME ZONE
) DISTSTYLE KEY DISTKEY (listid) SORTKEY (dateid)

