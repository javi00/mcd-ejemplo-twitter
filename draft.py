SELECT t.sender_id, t.text, t.timestamp 
FROM Tweets t 
JOIN Follows f ON f.user_followee_id = t.sender_id
JOIN Users u ON u.user_id = f.user_follow_id 
WHERE
u.user_id = 1
ORDER BY timestamp DESC;