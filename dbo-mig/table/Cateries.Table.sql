
CREATE TABLE Cateries (
  CateryID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY, 
  CateryName STRING NOT NULL, 
  Description STRING NULL, 
  Picture BINARY NULL
);
ALTER TABLE Cateries ADD CONSTRAINT PK_Cateries PRIMARY KEY (CateryID);
