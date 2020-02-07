show databases;
use university;
show tables;
Query 1;
select name,dept_name from student where ID = 12345;
select t.course_id,c.title,c.credits,t.grade from takes t join course c on c.course_id=t.course_id where ID =12345;
Query 2;
select course_id,title from course where title like '%en%';
Query 3;
select t.ID,s.name from takes t join student s on t.ID=s.ID where grade='F'  group by t.ID having count(t.ID)>=2;
Query 4;
insert into student values(12411,'chinmay','Maths & Computing',0);


select * from takes;
select * from course;
select * from student;
select * from grades;
select * from department where dept_name = 'Biology';
