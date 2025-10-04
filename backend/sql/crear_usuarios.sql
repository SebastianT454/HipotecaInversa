CREATE TABLE Users (
    id VARCHAR(20) NOT NULL PRIMARY KEY,
    age INT NOT NULL,
    gender TEXT NOT NULL,
    marital_status TEXT NOT NULL,
    spouse_age INT,
    spouse_gender TEXT,
    property_value DECIMAL NOT NULL,
    interest_rate DECIMAL NOT NULL
);
