
CREATE TABLE CustomerCustomerDemo (
  CustomerID STRING NOT NULL,
  CustomerTypeID STRING NOT NULL
);

ALTER TABLE CustomerCustomerDemo
ADD CONSTRAINT PK_CustomerCustomerDemo PRIMARY KEY (CustomerID, CustomerTypeID);

ALTER TABLE CustomerCustomerDemo
ADD FOREIGN KEY (CustomerTypeID) REFERENCES CustomerDemographics(CustomerTypeID);

ALTER TABLE CustomerCustomerDemo
ADD FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID);
