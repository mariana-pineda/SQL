
CREATE TABLE tickit.users (
	userid INTEGER NOT NULL, 
	username CHAR(8), 
	firstname VARCHAR(30), 
	lastname VARCHAR(30), 
	city VARCHAR(30), 
	state CHAR(2), 
	email VARCHAR(100), 
	phone CHAR(14), 
	likesports BOOLEAN, 
	liketheatre BOOLEAN, 
	likeconcerts BOOLEAN, 
	likejazz BOOLEAN, 
	likeclassical BOOLEAN, 
	likeopera BOOLEAN, 
	likerock BOOLEAN, 
	likevegas BOOLEAN, 
	likebroadway BOOLEAN, 
	likemusicals BOOLEAN
) DISTSTYLE KEY DISTKEY (userid) SORTKEY (userid)

