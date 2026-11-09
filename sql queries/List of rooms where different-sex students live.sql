-- List of rooms where different-sex students live
SELECT
	room
FROM
	students
GROUP BY
	room
HAVING 
	COUNT(DISTINCT sex) = 2
ORDER BY
	room;
