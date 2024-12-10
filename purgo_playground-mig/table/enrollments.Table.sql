
CREATE TABLE purgo_playground.enrollments (
    enrollment_id INT NOT NULL, 
    program_id INT NOT NULL, 
    enrollment_date TIMESTAMP
) USING DELTA

