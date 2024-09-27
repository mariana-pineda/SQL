
CREATE TABLE dbo.[Cateries] (
	[CateryID] INTEGER NOT NULL IDENTITY(1,1), 
	[CateryName] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[Description] NTEXT(1073741823) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Picture] IMAGE NULL, 
	CONSTRAINT [PK_Cateries] PRIMARY KEY ([CateryID])
)

