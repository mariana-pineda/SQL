
CREATE TABLE Cateries (
  CateryID INT GENERATED ALWAYS AS IDENTITY, 
  CateryName STRING NOT NULL, 
  Description STRING, 
  Picture BINARY, 
  PRIMARY KEY (CateryID)
)

