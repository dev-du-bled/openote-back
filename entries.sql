INSERT INTO "user" VALUES ( DEFAULT,'Student','1','he/him', 'student1@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'student', 'http://localhost:8000/images/logos/0.webp' );
INSERT INTO "user" VALUES ( DEFAULT,'Student','2','he/him', 'student2@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'student', 'http://localhost:8000/images/logos/1.webp' );
INSERT INTO "user" VALUES ( DEFAULT,'Admin','Admin','he/him', 'admin@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'admin', 'http://localhost:8000/images/logos/2.webp' );
INSERT INTO "user" VALUES ( DEFAULT,'Teacher', 'Teacher', 'he/him', 'teacher@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'teacher', 'http://localhost:8000/images/logos/3.webp' );

INSERT INTO "class" VALUES ( DEFAULT, 'BUT_1' );
INSERT INTO "class" VALUES ( DEFAULT, 'BUT_2' );
INSERT INTO "class" VALUES ( DEFAULT, 'BUT_3' );

INSERT INTO "group" VALUES ( DEFAULT, 'BUT_1_1' );
INSERT INTO "group" VALUES ( DEFAULT, 'BUT_1_2' );
INSERT INTO "group" VALUES ( DEFAULT, 'BUT_2_APP' );
INSERT INTO "group" VALUES ( DEFAULT, 'BUT_2_1' );
INSERT INTO "group" VALUES ( DEFAULT, 'BUT_2_2' );
INSERT INTO "group" VALUES ( DEFAULT, 'BUT_3_APP' );
INSERT INTO "group" VALUES ( DEFAULT, 'BUT_3_1' );
INSERT INTO "group" VALUES ( DEFAULT, 'BUT_3_2' );

INSERT INTO "unit" VALUES ( 'Maths' );
INSERT INTO "unit" VALUES ( 'Optimization' );
INSERT INTO "unit" VALUES ( 'Database Managment' );
INSERT INTO "unit" VALUES ( 'Web Dev' );

INSERT INTO "student_info" VALUES ( 1, 123456, 1, 1 );
INSERT INTO "student_info" VALUES ( 2, 120457, 2, 5 );

INSERT INTO "attendance" VALUES ( 1, 1, true, false, '', true );
INSERT INTO "attendance" VALUES ( 2, 2, true, true, 'Too late', false );

INSERT INTO "assigned_homework" VALUES ( DEFAULT, 'Finir le TP 1', '2021-01-12', 3, 'Finir le TP de la semaine 1', 1 );
INSERT INTO "assigned_homework" VALUES ( DEFAULT, 'Finir le TP 2', '2021-01-13', 3, 'Finir le TP de la semaine 2', 1 );
INSERT INTO "assigned_homework" VALUES ( DEFAULT, 'Finir le TP 3', '2022-05-14', 3, 'Finir le TP de la semaine 3', 1 );
INSERT INTO "assigned_homework" VALUES ( DEFAULT, 'Finir le TP 4', '2021-07-15', 3, 'Finir le TP de la semaine 4', 1 );
INSERT INTO "assigned_homework" VALUES ( DEFAULT, 'Finir le TP 5', '2021-08-16', 3, 'Finir le TP de la semaine 5', 1 );
INSERT INTO "assigned_homework" VALUES ( DEFAULT, 'Finir le TP 6', '2021-09-17', 3, 'Finir le TP de la semaine 6', 1 );
INSERT INTO "assigned_homework" VALUES ( DEFAULT, 'Finir le TP 7', '2021-12-18', 3, 'Finir le TP de la semaine 7', 2 );

INSERT INTO "homework_status" VALUES ( 1, 1, false );
INSERT INTO "homework_status" VALUES ( 2, 1, true );
INSERT INTO "homework_status" VALUES ( 3, 1, true );
INSERT INTO "homework_status" VALUES ( 4, 1, true );
INSERT INTO "homework_status" VALUES ( 5, 1, true );
INSERT INTO "homework_status" VALUES ( 6, 1, true );
INSERT INTO "homework_status" VALUES ( 7, 2, true );

INSERT INTO "exams" VALUES ( DEFAULT, 'Maths', 20, 1, '2021-12-12', 'Maths');
INSERT INTO "exams" VALUES ( DEFAULT, 'Optimization', 10, 2, '2021-12-13', 'Optimization');
INSERT INTO "exams" VALUES ( DEFAULT, 'Web Dev', 15, 3, '2021-12-14', 'Web Dev');
INSERT INTO "exams" VALUES ( DEFAULT, 'Database Managment', 5, 1, '2021-12-15', 'Database Managment');
INSERT INTO "exams" VALUES ( DEFAULT, 'Database Managment', 10, 2, '2021-12-16', 'Database Managment');
INSERT INTO "exams" VALUES ( DEFAULT, 'Database Managment', 15, 3, '2021-12-17', 'Database Managment');

INSERT INTO "marks" VALUES ( 2, 1, 15, DEFAULT );
INSERT INTO "marks" VALUES ( 2, 2, 10, DEFAULT );
INSERT INTO "marks" VALUES ( 2, 3, 15, DEFAULT );
INSERT INTO "marks" VALUES ( 2, 4, 5, DEFAULT );
INSERT INTO "marks" VALUES ( 2, 5, 10, DEFAULT );
INSERT INTO "marks" VALUES ( 2, 6, 15, DEFAULT );
INSERT INTO "marks" VALUES ( 1, 1, 15, DEFAULT );
INSERT INTO "marks" VALUES ( 1, 2, 10, DEFAULT );
INSERT INTO "marks" VALUES ( 1, 3, 15, DEFAULT );
INSERT INTO "marks" VALUES ( 1, 4, 5, DEFAULT );
INSERT INTO "marks" VALUES ( 1, 5, 10, DEFAULT );
INSERT INTO "marks" VALUES ( 1, 6, 15, DEFAULT );
