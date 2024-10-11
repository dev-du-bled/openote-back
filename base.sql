CREATE EXTENSION IF NOT EXISTS pg_cron;
GRANT USAGE ON SCHEMA cron TO openuser;


CREATE TYPE "role" AS ENUM (
	'parent',
	'student',
	'teacher',
	'admin'
);
CREATE TABLE "user" (
	"id" SERIAL NOT NULL UNIQUE,
	"lastname" VARCHAR NOT NULL,
	"firstname" VARCHAR NOT NULL,
	"pronouns" VARCHAR NOT NULL,
	"email" VARCHAR NOT NULL,
	"password_hash" VARCHAR NOT NULL,
	"role" ROLE NOT NULL,
	"profile_picture" VARCHAR,
	PRIMARY KEY("id")
);


CREATE TABLE "student_info" (
	"user_id" SERIAL NOT NULL UNIQUE,
	"student_number" INTEGER NOT NULL,
	"class" INTEGER NOT NULL,
	"group" INTEGER,
	PRIMARY KEY("user_id")
);


CREATE TABLE "notes" (
	"user_id" SERIAL NOT NULL UNIQUE,
	"exam_id" SERIAL NOT NULL UNIQUE,
	"commentaire" TEXT,
	"value" INTEGER NOT NULL,
	"max_value" INTEGER NOT NULL,
	"coefficient" DECIMAL DEFAULT 1,
	"date" DATE NOT NULL,
	PRIMARY KEY("user_id", "exam_id")
);


CREATE TABLE "attendance" (
	"class_id" SERIAL NOT NULL,
	"student_id" INTEGER NOT NULL,
	"present" BOOLEAN NOT NULL,
	"expelled" BOOLEAN DEFAULT false,
	"expell_reason" TEXT,
	"late" BOOLEAN DEFAULT false,
	PRIMARY KEY("class_id", "student_id")
);


CREATE TABLE "class" (
	"id" SERIAL NOT NULL UNIQUE,
	"name" VARCHAR NOT NULL UNIQUE,
	PRIMARY KEY("id")
);


CREATE TABLE "parent" (
	"parent_id" SERIAL NOT NULL UNIQUE,
	"user_id" INTEGER NOT NULL UNIQUE GENERATED BY DEFAULT AS IDENTITY,
	"child" INTEGER NOT NULL,
	PRIMARY KEY("parent_id")
);


CREATE TABLE "group" (
	"id" SERIAL NOT NULL UNIQUE,
	"name" VARCHAR UNIQUE,
	PRIMARY KEY("id")
);


CREATE TABLE "assigned_homework" (
	"id" SERIAL NOT NULL,
	"title" VARCHAR NOT NULL,
	"due_date" DATE NOT NULL,
	"author" INTEGER NOT NULL,
	"details" VARCHAR,
	"assigned_class" INTEGER,
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
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE "student_info"
ADD FOREIGN KEY("class") REFERENCES "class"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "student_info"
ADD FOREIGN KEY("group") REFERENCES "group"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "homework_status"
ADD FOREIGN KEY("homework") REFERENCES "assigned_homework"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "attendance"
ADD FOREIGN KEY("student_id") REFERENCES "student_info"("user_id")
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE "notes"
ADD FOREIGN KEY("user_id") REFERENCES "student_info"("user_id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "homework_status"
ADD FOREIGN KEY("student") REFERENCES "student_info"("user_id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "parent"
ADD FOREIGN KEY("child") REFERENCES "student_info"("user_id")
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE "sessions"
ADD FOREIGN KEY("associated_user") REFERENCES "user"("id")
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE "student_info"
ADD FOREIGN KEY("user_id") REFERENCES "user"("id")
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE "assigned_homework"
ADD FOREIGN KEY("assigned_class") REFERENCES "class"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;

SELECT cron.schedule('0 00 * * *', $$DELETE FROM sessions WHERE DATE_PART('EPOCH', expires_at) < (SELECT DATE_PART('EPOCH', CURRENT_TIMESTAMP));$$);
