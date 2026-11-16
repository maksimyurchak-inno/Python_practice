-- 5 rooms with the lowest average age of students
SELECT
    rooms.id AS room_id,
    rooms.name AS room_name,
    TO_CHAR(AVG(AGE(students.birthday)), 'YY "years" MM "months"') AS average_age
FROM rooms
JOIN students ON students.room = rooms.id
GROUP BY rooms.id, rooms.name
ORDER BY AVG(AGE(students.birthday)) ASC, rooms.id ASC
LIMIT 5;
