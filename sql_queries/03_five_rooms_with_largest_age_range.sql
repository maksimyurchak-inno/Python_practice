-- 5 rooms with the largest difference in the age of students
SELECT
    rooms.id AS room_id,
    rooms.name AS room_name,
    AGE(MAX(birthday), MIN(birthday))::text AS age_range  -- for convinient formatting
FROM rooms
JOIN students ON students.room = rooms.id
GROUP BY rooms.id, rooms.name
ORDER BY AGE(MAX(birthday), MIN(birthday)) DESC, rooms.id ASC
LIMIT 5;
