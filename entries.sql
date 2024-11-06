INSERT INTO "user" VALUES ( 0,'Davis','Terry','he/him', 'terry@temple.os', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'student', 'http://localhost:8000/images/logos/0.webp' );
INSERT INTO "user" VALUES ( 1,'admin','admin','he/him', 'admin@admin.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'admin', null );
INSERT INTO "user" VALUES ( 2,'Delavernhe', 'Florian', 'he/him', 'florian.delavernhe@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'teacher', 'http://localhost:8000/images/logos/2.webp' );
INSERT INTO "user" VALUES ( 3,'test','test','he/him', 'test@test.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'student', null );

INSERT INTO "class" VALUES ( 0, 'BUT_1' );
INSERT INTO "class" VALUES ( 1, 'BUT_2' );
INSERT INTO "class" VALUES ( 2, 'BUT_3' );

INSERT INTO "group" VALUES ( 0, 'BUT_1_APP' );
INSERT INTO "group" VALUES ( 1, 'BUT_1_1' );
INSERT INTO "group" VALUES ( 2, 'BUT_1_2' );

INSERT INTO "unit" VALUES ( 'Maths' );
INSERT INTO "unit" VALUES ( 'English' );
INSERT INTO "unit" VALUES ( 'Database managment' );
INSERT INTO "unit" VALUES ( 'Front End Dev' );

INSERT INTO "student_info" VALUES ( 0, 123456, 0, 1 );
INSERT INTO "student_info" VALUES ( 3, 120457, 1, 1 );

INSERT INTO "attendance" VALUES ( 0, 0, true, false, '', false );
INSERT INTO "attendance" VALUES ( 0, 3, true, true, 'puant', false );

INSERT INTO "assigned_homework" VALUES ( 0, 'Finir le TP 1', '2021-12-12', 2, 'Finir le TP de la semaine 3', 0 );
INSERT INTO "assigned_homework" VALUES ( 1, 'Finir le TP 2', '2021-12-12', 2, 'Finir le TP de la semaine 4', 1 );
INSERT INTO "assigned_homework" VALUES ( 2, 'Finir le TP 3', '2021-12-14', 2, 'Finir le TP de la semaine 5', 0 );
INSERT INTO "assigned_homework" VALUES ( 3, 'Finir le TP 4', '2021-12-15', 2, 'Finir le TP de la semaine 6', 0 );
INSERT INTO "assigned_homework" VALUES ( 4, 'Finir le TP 5', '2021-12-16', 2, 'Finir le TP de la semaine 7', 0 );
INSERT INTO "assigned_homework" VALUES ( 5, 'Finir le TP 6', '2021-12-17', 2, 'Finir le TP de la semaine 8', 0 );
INSERT INTO "assigned_homework" VALUES ( 6, 'Finir le TP 7', '2021-12-18', 2, 'Finir le TP de la semaine 9', 0 );

INSERT INTO "homework_status" VALUES ( 0, 0, false );
INSERT INTO "homework_status" VALUES ( 1, 3, true );
INSERT INTO "homework_status" VALUES ( 2, 0, true );
INSERT INTO "homework_status" VALUES ( 3, 0, true );
INSERT INTO "homework_status" VALUES ( 4, 0, true );
INSERT INTO "homework_status" VALUES ( 5, 0, true );
INSERT INTO "homework_status" VALUES ( 6, 0, true );

INSERT INTO "exams" VALUES ( 0, 'Système', 20, 1, '2021-12-12', 'Maths');
INSERT INTO "exams" VALUES ( 1, 'Réseau', 10, 2, '2021-12-13', 'English');
INSERT INTO "exams" VALUES ( 2, 'Web', 15, 3, '2021-12-14', 'Database managment');
INSERT INTO "exams" VALUES ( 3, 'Math', 5, 1, '2021-12-15', 'Front End Dev');
INSERT INTO "exams" VALUES ( 4, 'Anglais', 10, 2, '2021-12-16', 'Maths');
INSERT INTO "exams" VALUES ( 5, 'Français', 15, 3, '2021-12-17', 'English');

INSERT INTO "marks" VALUES ( 3, 0, 15 );
INSERT INTO "marks" VALUES ( 3, 1, 10 );
INSERT INTO "marks" VALUES ( 3, 2, 15 );
INSERT INTO "marks" VALUES ( 3, 3, 5 );
INSERT INTO "marks" VALUES ( 3, 4, 10 );
INSERT INTO "marks" VALUES ( 3, 5, 15 );
INSERT INTO "marks" VALUES ( 0, 0, 15 );
INSERT INTO "marks" VALUES ( 0, 1, 10 );
INSERT INTO "marks" VALUES ( 0, 2, 15 );
INSERT INTO "marks" VALUES ( 0, 3, 5 );
INSERT INTO "marks" VALUES ( 0, 4, 10 );
INSERT INTO "marks" VALUES ( 0, 5, 15 );
