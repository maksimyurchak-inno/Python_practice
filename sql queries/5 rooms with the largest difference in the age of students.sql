-- 5 rooms with the largest difference in the age of students
SELECT
	room
FROM 
	students
GROUP BY 
	room
ORDER BY
	MAX(birthday) - MIN(birthday) DESC
LIMIT 5;
