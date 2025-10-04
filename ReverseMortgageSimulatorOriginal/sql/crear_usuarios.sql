CREATE TABLE Users (
    id VARCHAR(20) NOT NULL PRIMARY KEY,
    age VARCHAR(2) NOT NULL,
    marital_status TEXT NOT NULL,
    spouse_age VARCHAR(2),
    spouse_gender TEXT,
    property_value VARCHAR(20) NOT NULL,
    interest_rate VARCHAR(4) NOT NULL
);
