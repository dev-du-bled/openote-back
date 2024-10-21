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

INSERT INTO "student_info" VALUES ( 0, 123456, 1, 1 );
INSERT INTO "student_info" VALUES ( 3, 120457, 1, 1 );

INSERT INTO "attendance" VALUES ( 0, 0, true, false, '', false );
INSERT INTO "attendance" VALUES ( 0, 3, true, true, 'puant', false );

INSERT INTO "exams" VALUES ( 0, 'Système', 20, 1, '2021-12-12' );
INSERT INTO "exams" VALUES ( 1, 'Réseau', 10, 2, '2021-12-13' );

INSERT INTO "marks" VALUES ( 3, 0, 15 );
INSERT INTO "marks" VALUES ( 0, 1, 5 );