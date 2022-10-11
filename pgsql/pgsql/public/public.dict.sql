
-- 字典表
DROP TABLE IF EXISTS "public"."dictionary";

CREATE TABLE IF NOT EXISTS "public"."dictionary" (
	"id" serial NOT NULL,
	"creator" int not null DEFAULT 0,
	"create_time" timestamp NOT NULL DEFAULT NOW(),
	"operator" int not null DEFAULT 0,
	"operat_time" timestamp NOT NULL DEFAULT NOW(),
	"is_delete" bool NOT NULL DEFAULT False,
	"organize" varchar NOT NULL,
	"organize_tab" varchar NOT NULL DEFAULT 'Unk',
	"options_value" varchar NOT NULL,
	"options_label" varchar NOT NULL,
	"father_value" varchar DEFAULT NULL,
	CONSTRAINT public_dictionary_pk PRIMARY KEY ("id")
);
COMMENT ON TABLE "public"."dictionary" IS '公共字典表';

CREATE INDEX idx_dictionary_organize
ON "public"."dictionary" ("organize");

CREATE UNIQUE INDEX uk_dictionary_organize
ON "public"."dictionary" ("organize","options_value");


CREATE TRIGGER "public_dictionary_operate" BEFORE UPDATE ON "public"."dictionary" FOR EACH ROW EXECUTE PROCEDURE operat_time();
COMMENT ON COLUMN "public"."dictionary".organize IS '字典编组';
COMMENT ON COLUMN "public"."dictionary".options_value IS '选项值';
COMMENT ON COLUMN "public"."dictionary".options_label IS '选项标签';
COMMENT ON COLUMN "public"."dictionary".father_value IS '先后关联值';

INSERT INTO "public"."dictionary" ("creator", "create_time", "operator", "operat_time", "is_delete", "organize", "options_value", "options_label","organize_tab") 
VALUES (0, '2021-09-22 09:13:14.135749', 0, '2021-09-22 09:17:40.777802', 'f', 'SEX', 'boy', '男', '性别');

INSERT INTO "public"."dictionary" ("creator", "create_time", "operator", "operat_time", "is_delete", "organize", "options_value", "options_label","organize_tab") 
VALUES (0, '2021-09-22 09:13:14.135749', 0, '2021-09-22 09:17:44.093328', 'f', 'SEX', 'girl', '女', '性别');