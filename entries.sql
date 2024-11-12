INSERT INTO "user" VALUES ( 0,'Student','1','he/him', 'student1@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'student', 'http://localhost:8000/images/logos/0.webp' );
INSERT INTO "user" VALUES ( 1,'Student','2','he/him', 'student2@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'student', 'http://localhost:8000/images/logos/1.webp' );
INSERT INTO "user" VALUES ( 2,'Admin','Admin','he/him', 'admin@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'admin', 'http://localhost:8000/images/logos/2.webp' );
INSERT INTO "user" VALUES ( 3,'Teacher', 'Teacher', 'he/him', 'teacher@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'teacher', 'http://localhost:8000/images/logos/3.webp' );

INSERT INTO "class" VALUES ( 0, 'BUT_1' );
INSERT INTO "class" VALUES ( 1, 'BUT_2' );
INSERT INTO "class" VALUES ( 2, 'BUT_3' );

INSERT INTO "group" VALUES ( 0, 'BUT_1_1' );
INSERT INTO "group" VALUES ( 1, 'BUT_1_2' );
INSERT INTO "group" VALUES ( 2, 'BUT_2_APP' );
INSERT INTO "group" VALUES ( 3, 'BUT_2_1' );
INSERT INTO "group" VALUES ( 4, 'BUT_2_2' );
INSERT INTO "group" VALUES ( 5, 'BUT_3_APP' );
INSERT INTO "group" VALUES ( 6, 'BUT_3_1' );
INSERT INTO "group" VALUES ( 7, 'BUT_3_2' );

INSERT INTO "unit" VALUES ( 'Maths' );
INSERT INTO "unit" VALUES ( 'Optimization' );
INSERT INTO "unit" VALUES ( 'Database Managment' );
INSERT INTO "unit" VALUES ( 'Web Dev' );

INSERT INTO "student_info" VALUES ( 0, 123456, 0, 0 );
INSERT INTO "student_info" VALUES ( 1, 120457, 1, 4 );

INSERT INTO "attendance" VALUES ( 0, 0, true, false, '', true );
INSERT INTO "attendance" VALUES ( 1, 1, true, true, 'Too late', false );

INSERT INTO "assigned_homework" VALUES ( 0, 'Finir le TP 1', '2021-01-12', 3, 'Finir le TP de la semaine 1', 0 );
INSERT INTO "assigned_homework" VALUES ( 1, 'Finir le TP 2', '2021-01-13', 3, 'Finir le TP de la semaine 2', 0 );
INSERT INTO "assigned_homework" VALUES ( 2, 'Finir le TP 3', '2022-05-14', 3, 'Finir le TP de la semaine 3', 0 );
INSERT INTO "assigned_homework" VALUES ( 3, 'Finir le TP 4', '2021-07-15', 3, 'Finir le TP de la semaine 4', 0 );
INSERT INTO "assigned_homework" VALUES ( 4, 'Finir le TP 5', '2021-08-16', 3, 'Finir le TP de la semaine 5', 0 );
INSERT INTO "assigned_homework" VALUES ( 5, 'Finir le TP 6', '2021-09-17', 3, 'Finir le TP de la semaine 6', 0 );
INSERT INTO "assigned_homework" VALUES ( 6, 'Finir le TP 7', '2021-12-18', 3, 'Finir le TP de la semaine 7', 1 );

INSERT INTO "homework_status" VALUES ( 0, 0, false );
INSERT INTO "homework_status" VALUES ( 1, 0, true );
INSERT INTO "homework_status" VALUES ( 2, 0, true );
INSERT INTO "homework_status" VALUES ( 3, 0, true );
INSERT INTO "homework_status" VALUES ( 4, 0, true );
INSERT INTO "homework_status" VALUES ( 5, 0, true );
INSERT INTO "homework_status" VALUES ( 6, 1, true );

INSERT INTO "exams" VALUES ( 0, 'Maths', 20, 1, '2021-12-12', 'Maths');
INSERT INTO "exams" VALUES ( 1, 'Optimization', 10, 2, '2021-12-13', 'Optimization');
INSERT INTO "exams" VALUES ( 2, 'Web Dev', 15, 3, '2021-12-14', 'Web Dev');
INSERT INTO "exams" VALUES ( 3, 'Database Managment', 5, 1, '2021-12-15', 'Database Managment');
INSERT INTO "exams" VALUES ( 4, 'Database Managment', 10, 2, '2021-12-16', 'Database Managment');
INSERT INTO "exams" VALUES ( 5, 'Database Managment', 15, 3, '2021-12-17', 'Database Managment');

INSERT INTO "marks" VALUES ( 1, 0, 15 );
INSERT INTO "marks" VALUES ( 1, 1, 10 );
INSERT INTO "marks" VALUES ( 1, 2, 15 );
INSERT INTO "marks" VALUES ( 1, 3, 5 );
INSERT INTO "marks" VALUES ( 1, 4, 10 );
INSERT INTO "marks" VALUES ( 1, 5, 15 );
INSERT INTO "marks" VALUES ( 0, 0, 15 );
INSERT INTO "marks" VALUES ( 0, 1, 10 );
INSERT INTO "marks" VALUES ( 0, 2, 15 );
INSERT INTO "marks" VALUES ( 0, 3, 5 );
INSERT INTO "marks" VALUES ( 0, 4, 10 );
INSERT INTO "marks" VALUES ( 0, 5, 15 );
