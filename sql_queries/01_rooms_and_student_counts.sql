-- List of rooms and the number of students in each of them
SELECT
    rooms.id AS room_id,
    rooms.name AS room_name,
    COUNT(students.id) AS student_count
FROM rooms
LEFT JOIN students ON students.room = rooms.id
GROUP BY rooms.id, rooms.name
ORDER BY rooms.id;
