-- 5 rooms with the smallest average age of students
SELECT
	room
FROM 
	students
GROUP BY 
	room
ORDER BY
	AVG(AGE(birthday)) ASC
LIMIT 5;
