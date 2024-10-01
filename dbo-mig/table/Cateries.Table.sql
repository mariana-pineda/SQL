
CREATE TABLE Cateries (
  CateryID INT NOT NULL, 
  CateryName STRING NOT NULL, 
  Description STRING, 
  Picture BINARY, 
  PRIMARY KEY (CateryID)
);

CREATE SEQUENCE CateryID_seq START WITH 1 INCREMENT BY 1;

CREATE TRIGGER before_insert_Cateries
BEFORE INSERT ON Cateries
FOR EACH ROW
SET NEW.CateryID = nextval('CateryID_seq');
