
CREATE TABLE CustomerCustomerDemo (
  CustomerID STRING NOT NULL,
  CustomerTypeID STRING NOT NULL
);

-- Adding Primary Key Constraint
ALTER TABLE CustomerCustomerDemo
ADD CONSTRAINT PK_CustomerCustomerDemo
PRIMARY KEY (CustomerID, CustomerTypeID);

-- Adding Foreign Key Constraints
ALTER TABLE CustomerCustomerDemo
ADD CONSTRAINT FK_CustomerCustomerDemo
FOREIGN KEY (CustomerTypeID) REFERENCES CustomerDemographics (CustomerTypeID);

ALTER TABLE CustomerCustomerDemo
ADD CONSTRAINT FK_CustomerCustomerDemo_Customers
FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);
