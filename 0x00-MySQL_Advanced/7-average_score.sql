-- Create a stored procedure ComputeAverageScoreForUser that computes and stores the average score for a student

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE v_avg_score FLOAT;

    -- Compute the average score
    SELECT AVG(score) INTO v_avg_score
    FROM corrections
    WHERE user_id = p_user_id;

    -- Update the user's average_score
    UPDATE users
    SET average_score = IFNULL(v_avg_score, 0)
    WHERE id = p_user_id;
END //

DELIMITER ;