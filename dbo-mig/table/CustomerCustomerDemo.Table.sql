
CREATE TABLE CustomerCustomerDemo (
    CustomerID STRING NOT NULL, 
    CustomerTypeID STRING NOT NULL, 
    PRIMARY KEY (CustomerID, CustomerTypeID), 
    FOREIGN KEY (CustomerTypeID) REFERENCES CustomerDemographics (CustomerTypeID), 
    FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID)
)
