# Note that there must be 2 sections: @Up and @down
# All SQL must be terminated with a semi column (";")
# Do not touch this file! To create a new migration, see README.md

@Up
CREATE TABLE migrations (id BIGSERIAL PRIMARY KEY, title VARCHAR(128), applied_at TIMESTAMP DEFAULT NOW());

@Down
DROP TABLE migrations;