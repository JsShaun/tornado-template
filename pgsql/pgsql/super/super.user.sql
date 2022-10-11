

-- 用户
DROP TABLE IF EXISTS "super"."user";

CREATE TABLE IF NOT EXISTS "super"."user" (
	id serial NOT NULL,
	phone varchar NOT NULL, -- 电话
	email varchar NOT NULL, -- 邮箱
	pass_word varchar NOT NULL, -- 密码
	last_time timestamp NULL, -- 最后登陆时间
	creator int not null DEFAULT 0,
	create_time timestamp NOT NULL DEFAULT NOW(),
	operator int not null DEFAULT 0,
	operat_time timestamp NOT NULL DEFAULT NOW(),
	is_delete bool NOT NULL DEFAULT False,
	CONSTRAINT user_pk PRIMARY KEY (id)
);
COMMENT ON TABLE "super"."user" IS '管理员';
CREATE TRIGGER "super_user_operate" BEFORE UPDATE ON "super"."user" FOR EACH ROW EXECUTE PROCEDURE operat_time();
-- Column comments

CREATE INDEX idx_user_email
ON "super"."user" ("email");

CREATE INDEX idx_user_creator
ON "super"."user" ("creator");


CREATE INDEX idx_user_phone
ON "super"."user" ("phone");

COMMENT ON COLUMN "super"."user".phone IS '电话';
COMMENT ON COLUMN "super"."user".email IS '邮箱';
COMMENT ON COLUMN "super"."user".pass_word IS '密码';
COMMENT ON COLUMN "super"."user".last_time IS '最后登陆时间';


-- Permissions

ALTER TABLE "super"."user" OWNER TO postgres;
GRANT ALL ON TABLE "super"."user" TO postgres;



INSERT INTO "super"."user"(phone, email, pass_word, last_time)VALUES ('13333333333', '77254@qq.com','123456', NOW());







