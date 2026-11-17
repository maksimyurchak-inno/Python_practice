-- 5 rooms with the largest difference in the age of students
SELECT
    rooms.id AS room_id,
    rooms.name AS room_name,
    (MAX(birthday) - MIN(birthday)) AS age_range  
FROM rooms
JOIN students ON students.room = rooms.id
GROUP BY rooms.id, rooms.name
HAVING COUNT(students.id) > 1
ORDER BY AGE(MAX(birthday), MIN(birthday)) DESC, rooms.id ASC
LIMIT 5;
