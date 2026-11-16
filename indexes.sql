-- (room, birthday) starts with the join key and includes the date used by the age reports.
CREATE INDEX IF NOT EXISTS idx_students_room_birthday
    ON students (room, birthday);

-- (room, sex) starts with the join key and includes the value checked by the mixed-sex report.
CREATE INDEX IF NOT EXISTS idx_students_room_sex
    ON students (room, sex);
