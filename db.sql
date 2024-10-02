CREATE TYPE "role" AS ENUM (
	'parent',
	'student',
	'teacher',
	'admin'
);
CREATE TABLE "user" (
	"id" INTEGER NOT NULL UNIQUE,
	"lastname" VARCHAR NOT NULL,
	"firstname" VARCHAR NOT NULL,
	"pronouns" VARCHAR NOT NULL,
	"email" VARCHAR NOT NULL,
	"password_hash" VARCHAR NOT NULL,
	"role" ROLE NOT NULL,
	"profile_picture" BYTEA,
	PRIMARY KEY("id")
);


CREATE TABLE "student_info" (
	"user_id" INTEGER NOT NULL UNIQUE,
	"student_number" INTEGER NOT NULL,
	"class" INTEGER NOT NULL UNIQUE,
	"group" INTEGER UNIQUE,
	PRIMARY KEY("user_id")
);


CREATE TABLE "notes" (
	"user_id" INTEGER NOT NULL UNIQUE,
	"exam_id" INTEGER NOT NULL UNIQUE,
	"commentaire" TEXT,
	"value" INTEGER NOT NULL,
	"max_value" INTEGER NOT NULL,
	"coefficient" DECIMAL DEFAULT 1,
	"date" DATE NOT NULL,
	PRIMARY KEY("user_id", "exam_id")
);


CREATE TABLE "attendance" (
	"class_id" INTEGER NOT NULL,
	"student_id" INTEGER NOT NULL UNIQUE,
	"present" BOOLEAN NOT NULL,
	"expelled" BOOLEAN DEFAULT false,
	"expel_reason" TEXT,
	"late" BOOLEAN DEFAULT false,
	PRIMARY KEY("class_id", "student_id")
);


CREATE TABLE "class" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" VARCHAR NOT NULL,
	PRIMARY KEY("id")
);


CREATE TABLE "parent" (
	"parent_id" INTEGER NOT NULL UNIQUE,
	"user_id" INTEGER NOT NULL UNIQUE,
	"child" INTEGER NOT NULL,
	PRIMARY KEY("parent_id")
);


CREATE TABLE "groups" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" VARCHAR,
	PRIMARY KEY("id")
);


CREATE TABLE "assigned_homework" (
	"id" INTEGER,
	"title" VARCHAR NOT NULL,
	"due_date" DATE NOT NULL,
	"teacher" INTEGER NOT NULL,
	"details" VARCHAR,
	PRIMARY KEY("id")
);


CREATE TABLE "homework_status" (
	"homework" INTEGER NOT NULL UNIQUE,
	"student" INTEGER NOT NULL UNIQUE,
	"is_done" BOOLEAN NOT NULL,
	PRIMARY KEY("homework", "student")
);


CREATE TABLE "sessions" (
	"token" VARCHAR NOT NULL UNIQUE,
	"associated_user" INTEGER NOT NULL,
	"expires_at" TIMESTAMP NOT NULL,
	"extended_period" BOOLEAN NOT NULL DEFAULT false,
	PRIMARY KEY("token")
);


ALTER TABLE "parent"
ADD FOREIGN KEY("user_id") REFERENCES "user"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "student_info"
ADD FOREIGN KEY("class") REFERENCES "class"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "student_info"
ADD FOREIGN KEY("group") REFERENCES "groups"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "homework_status"
ADD FOREIGN KEY("homework") REFERENCES "assigned_homework"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "attendance"
ADD FOREIGN KEY("student_id") REFERENCES "student_info"("user_id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "notes"
ADD FOREIGN KEY("user_id") REFERENCES "student_info"("user_id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "homework_status"
ADD FOREIGN KEY("student") REFERENCES "student_info"("user_id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "parent"
ADD FOREIGN KEY("child") REFERENCES "student_info"("user_id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "sessions"
ADD FOREIGN KEY("associated_user") REFERENCES "user"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "student_info"
ADD FOREIGN KEY("user_id") REFERENCES "user"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;

INSERT INTO "user" VALUES ( 0,'Davis','Terry','he/him', 'terry@temple.os', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'student', null );
