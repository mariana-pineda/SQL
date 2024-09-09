
CREATE TABLE tickit.category (
	catid SMALLINT NOT NULL, 
	catgroup VARCHAR(10), 
	catname VARCHAR(10), 
	catdesc VARCHAR(50)
) DISTSTYLE KEY DISTKEY (catid) SORTKEY (catid)

