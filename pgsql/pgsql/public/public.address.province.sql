-- ----------------------------
-- Table structure for province
-- ----------------------------
DROP TABLE IF EXISTS "public"."province";
CREATE TABLE "public"."province" (
  "province_code" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "province_name" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "is_delete" bool NOT NULL,
  "id" int2 NOT NULL DEFAULT nextval('province_id_seq'::regclass),
  "is_open" bool NOT NULL DEFAULT false
);



-- ----------------------------
-- Records of province
-- ----------------------------
INSERT INTO "public"."province" VALUES ('11', '北京市', 'f', 1, 't');
INSERT INTO "public"."province" VALUES ('12', '天津市', 'f', 2, 't');
INSERT INTO "public"."province" VALUES ('13', '河北省', 'f', 3, 't');
INSERT INTO "public"."province" VALUES ('14', '山西省', 'f', 4, 't');
INSERT INTO "public"."province" VALUES ('15', '内蒙古自治区', 'f', 5, 't');
INSERT INTO "public"."province" VALUES ('21', '辽宁省', 'f', 6, 't');
INSERT INTO "public"."province" VALUES ('22', '吉林省', 'f', 7, 't');
INSERT INTO "public"."province" VALUES ('23', '黑龙江省', 'f', 8, 't');
INSERT INTO "public"."province" VALUES ('31', '上海市', 'f', 9, 't');
INSERT INTO "public"."province" VALUES ('32', '江苏省', 'f', 10, 't');
INSERT INTO "public"."province" VALUES ('33', '浙江省', 'f', 11, 't');
INSERT INTO "public"."province" VALUES ('34', '安徽省', 'f', 12, 't');
INSERT INTO "public"."province" VALUES ('35', '福建省', 'f', 13, 't');
INSERT INTO "public"."province" VALUES ('36', '江西省', 'f', 14, 't');
INSERT INTO "public"."province" VALUES ('41', '河南省', 'f', 15, 't');
INSERT INTO "public"."province" VALUES ('42', '湖北省', 'f', 16, 't');
INSERT INTO "public"."province" VALUES ('43', '湖南省', 'f', 17, 't');
INSERT INTO "public"."province" VALUES ('44', '广东省', 'f', 18, 't');
INSERT INTO "public"."province" VALUES ('45', '广西壮族自治区', 'f', 19, 't');
INSERT INTO "public"."province" VALUES ('46', '海南省', 'f', 20, 't');
INSERT INTO "public"."province" VALUES ('50', '重庆市', 'f', 21, 't');
INSERT INTO "public"."province" VALUES ('51', '四川省', 'f', 22, 't');
INSERT INTO "public"."province" VALUES ('52', '贵州省', 'f', 23, 't');
INSERT INTO "public"."province" VALUES ('53', '云南省', 'f', 24, 't');
INSERT INTO "public"."province" VALUES ('54', '西藏自治区', 'f', 25, 't');
INSERT INTO "public"."province" VALUES ('61', '陕西省', 'f', 26, 't');
INSERT INTO "public"."province" VALUES ('62', '甘肃省', 'f', 27, 't');
INSERT INTO "public"."province" VALUES ('63', '青海省', 'f', 28, 't');
INSERT INTO "public"."province" VALUES ('64', '宁夏回族自治区', 'f', 29, 't');
INSERT INTO "public"."province" VALUES ('65', '新疆维吾尔自治区', 'f', 30, 't');
INSERT INTO "public"."province" VALUES ('71', '台湾省', 'f', 31, 't');
INSERT INTO "public"."province" VALUES ('81', '香港特别行政区', 'f', 32, 't');
INSERT INTO "public"."province" VALUES ('82', '澳门特别行政区', 'f', 33, 't');
INSERT INTO "public"."province" VALUES ('37', '山东省', 'f', 34, 't');

-- ----------------------------
-- Primary Key structure for table province
-- ----------------------------
ALTER TABLE "public"."province" ADD CONSTRAINT "province_pkey" PRIMARY KEY ("id");
