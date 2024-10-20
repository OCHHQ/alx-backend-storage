-- Create a trigger that resets the attribute valid_email only when the email has been changed.
-- This trigger will fire before an update operation on the users table.

DELIMITER //

CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email field is being updated
    IF NEW.email != OLD.email THEN
        -- If email is changed, set valid_email to 0
        SET NEW.valid_email = 0;
    END IF;
END //

DELIMITER ;