--
-- File generated with SQLiteStudio v3.3.3 on Fri Oct 1 23:25:38 2021
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: courses
CREATE TABLE IF NOT EXISTS  courses (id VARCHAR PRIMARY KEY, name TEXT);

-- Table: instructors
CREATE TABLE IF NOT EXISTS  instructors (id INTEGER PRIMARY KEY, name TEXT, course_id VARCHAR REFERENCES courses (id) ON DELETE CASCADE ON UPDATE CASCADE MATCH SIMPLE);

-- Table: room
CREATE TABLE IF NOT EXISTS  room (id INT PRIMARY KEY, name TEXT, component VARCHAR);

-- Table: students
CREATE TABLE IF NOT EXISTS  `students` (
                    `id` INTEGER PRIMARY KEY,
                    `year` INTEGER,
                    `term` INTEGER,
                    `program` text,
                    `tot_enroll_planned` INTEGER,
                    `pland_stds` INTEGER,
                    `pattern` INTEGER
                    );

-- View: course_dashboard
CREATE VIEW IF NOT EXISTS  course_dashboard AS with course_patterns_room as 
(select course_id, 
pattern,
class_hrs, 
NULL as lab_hrs,
1 as room_id 
from patterns
union
select course_id, 
pattern,
NULL, 
lab_hrs ,
2 as room_id
from patterns 
where lab_hrs is not null),
base_tab as (
select s.program||' '||c.name as course_id,
cs.num_sections,
s.pland_stds as planned_students,
r.component as component,
coalesce(cpr.class_hrs, cpr.lab_hrs) as hrs_p_wk,
cpr.pattern,
r.name as room_type,
null as final_exam,
i.name as recommended_instructor
from students s 
inner join course_patterns_room cpr
on s.program = cpr.course_id
inner join course_sections cs
on cs.course_id = s.program
inner join room r 
on r.id = cpr.room_id
inner join instructors i
on i.course_id = s.program
inner join courses c
on c.id = s.program
),
t as (
     select course_id, 1 as section, planned_students, component, hrs_p_wk,pattern,room_type, final_exam, recommended_instructor, num_sections
     from base_tab 
     union all
     select course_id, section + 1, planned_students, component, hrs_p_wk,pattern,room_type, final_exam, recommended_instructor, num_sections
     from t
     where section < num_sections
 ) 
select course_id, section, planned_students, component, hrs_p_wk,pattern,room_type, final_exam, recommended_instructor
from t
order by 1;

-- View: course_sections
CREATE VIEW IF NOT EXISTS  course_sections as
select 
program as course_id,
cast((cast(tot_enroll_planned as float)/ pland_stds)+0.9 as int) as num_sections
from students;

-- View: patterns
CREATE VIEW IF NOT EXISTS  patterns AS select program as course_id, 
pattern, 
substr(pattern, 0, instr(pattern,'-')) as class_hrs, 
substr(pattern, instr(pattern,'-')+1, length(pattern)) as lab_hrs  
from students 
where instr(pattern, '-')
union
select program as course_id, 
pattern, 
pattern as class_hrs, 
NULL as lab_hrs 
from students 
where not instr(pattern, '-');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
