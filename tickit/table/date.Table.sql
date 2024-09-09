
CREATE TABLE tickit.date (
	dateid SMALLINT NOT NULL, 
	caldate DATE NOT NULL, 
	day CHAR(3) NOT NULL, 
	week SMALLINT NOT NULL, 
	month CHAR(5) NOT NULL, 
	qtr CHAR(5) NOT NULL, 
	year SMALLINT NOT NULL, 
	holiday BOOLEAN DEFAULT false
) DISTSTYLE KEY DISTKEY (dateid) SORTKEY (dateid)

