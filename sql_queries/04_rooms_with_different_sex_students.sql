-- List of rooms where different-sex students live
SELECT
    rooms.id AS room_id,
    rooms.name AS room_name
FROM rooms
JOIN students ON students.room = rooms.id
GROUP BY rooms.id, rooms.name
HAVING COUNT(DISTINCT students.sex) > 1
ORDER BY rooms.id;
