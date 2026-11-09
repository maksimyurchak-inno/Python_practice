-- List of rooms and the number of students in each of them
SELECT
	room,
	COUNT(name)
FROM
	students
GROUP BY
	room
ORDER BY
	room;
