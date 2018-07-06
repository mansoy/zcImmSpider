/*
 Navicat Premium Data Transfer

 Source Server         : 114.116.22.68
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : 114.116.22.68:3306
 Source Schema         : zc_data

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 06/07/2018 17:44:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for b_area
-- ----------------------------
DROP TABLE IF EXISTS `b_area`;
CREATE TABLE `b_area`  (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '分区名称',
  `desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for b_country
-- ----------------------------
DROP TABLE IF EXISTS `b_country`;
CREATE TABLE `b_country`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `aid` bigint(20) NULL DEFAULT NULL COMMENT '赛事分区编号',
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 241 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for b_lmatch
-- ----------------------------
DROP TABLE IF EXISTS `b_lmatch`;
CREATE TABLE `b_lmatch`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `cid` bigint(20) NULL DEFAULT NULL COMMENT '国家名称(二级分类)',
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '简称',
  `fullname` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '全称',
  `remark` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '描述',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `index2`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10986 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for b_lottery
-- ----------------------------
DROP TABLE IF EXISTS `b_lottery`;
CREATE TABLE `b_lottery`  (
  `id` bigint(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fullname` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `remark` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `index2`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2627368 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for b_team
-- ----------------------------
DROP TABLE IF EXISTS `b_team`;
CREATE TABLE `b_team`  (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fullname` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `remark` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3162 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for b_website
-- ----------------------------
DROP TABLE IF EXISTS `b_website`;
CREATE TABLE `b_website`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  `desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for bfodds
-- ----------------------------
DROP TABLE IF EXISTS `bfodds`;
CREATE TABLE `bfodds`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `mid` varchar(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL COMMENT '比赛场次',
  `lyid` int(11) NULL DEFAULT NULL COMMENT '博彩公司编号',
  `mw10` float NULL DEFAULT NULL COMMENT '主胜1:0',
  `mw20` float NULL DEFAULT NULL COMMENT '主胜2:0',
  `mw21` float NULL DEFAULT NULL COMMENT '主胜2:1',
  `mw30` float NULL DEFAULT NULL COMMENT '主胜3:0',
  `mw31` float NULL DEFAULT NULL COMMENT '主胜3:1',
  `mw32` float NULL DEFAULT NULL COMMENT '主胜3:2',
  `mw40` float NULL DEFAULT NULL COMMENT '主胜4:0',
  `mw41` float NULL DEFAULT NULL COMMENT '主胜4:1',
  `mw42` float NULL DEFAULT NULL COMMENT '主胜4:2',
  `mw43` float NULL DEFAULT NULL COMMENT '主胜4:3',
  `dw10` float NULL DEFAULT NULL COMMENT '客胜1:0',
  `dw20` float NULL DEFAULT NULL COMMENT '客胜2:0',
  `dw21` float NULL DEFAULT NULL COMMENT '客胜2:1',
  `dw30` float NULL DEFAULT NULL COMMENT '客胜3:0',
  `dw31` float NULL DEFAULT NULL COMMENT '客胜3:1',
  `dw32` float NULL DEFAULT NULL COMMENT '客胜3:2',
  `dw40` float NULL DEFAULT NULL COMMENT '客胜4:0',
  `dw41` float NULL DEFAULT NULL COMMENT '客胜4:1',
  `dw42` float NULL DEFAULT NULL COMMENT '客胜4:2',
  `dw43` float NULL DEFAULT NULL COMMENT '客胜4:3',
  `d00` float NULL DEFAULT NULL COMMENT '平0:0',
  `d11` float NULL DEFAULT NULL COMMENT '平1:1',
  `d22` float NULL DEFAULT NULL COMMENT '平2:2',
  `d33` float NULL DEFAULT NULL COMMENT '平3:3',
  `d44` float NULL DEFAULT NULL COMMENT '平4:4',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `mid`(`mid`, `lyid`) USING BTREE,
  INDEX `mid_2`(`mid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11113 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for intermatch
-- ----------------------------
DROP TABLE IF EXISTS `intermatch`;
CREATE TABLE `intermatch`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `lsid` int(11) NULL DEFAULT NULL COMMENT '联赛编号',
  `season` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '赛季',
  `group` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '组名',
  `stage` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '比赛阶段(如: 小组赛, 16强等)',
  `index` int(10) NOT NULL COMMENT '序号',
  `mid` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '比赛编号',
  `mtid` int(11) NULL DEFAULT NULL COMMENT '主队编号',
  `mscore` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '主队得分',
  `dtid` int(11) NULL DEFAULT NULL COMMENT '副队编号',
  `dscore` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '副队得分',
  `mdate` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '比赛日期',
  `mtime` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '比赛时间',
  `status` int(10) NULL DEFAULT 0 COMMENT '比赛状态',
  `status_desc` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '状态描述',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `mid`(`mid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for lsscore
-- ----------------------------
DROP TABLE IF EXISTS `lsscore`;
CREATE TABLE `lsscore`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `season` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '赛季',
  `lsid` bigint(20) NULL DEFAULT NULL COMMENT '赛事编号',
  `tid` bigint(20) NULL DEFAULT NULL COMMENT '球队编号',
  `mtimes` int(11) NULL DEFAULT NULL COMMENT '参加比赛的场次数量',
  `wtimes` int(11) NULL DEFAULT NULL COMMENT '胜场次数',
  `etimes` int(11) NULL DEFAULT NULL COMMENT '平场次数',
  `ltimes` int(11) NULL DEFAULT NULL COMMENT '负场次数',
  `score` int(11) NULL DEFAULT NULL COMMENT '积分',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `lmid`(`lsid`, `tid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2874 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci COMMENT = '联赛球队积分表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for matchdata
-- ----------------------------
DROP TABLE IF EXISTS `matchdata`;
CREATE TABLE `matchdata`  (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `mid` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '比赛场次编号',
  `ssid` int(11) NOT NULL DEFAULT 0 COMMENT '赛季编号',
  `mtid` int(11) NOT NULL COMMENT '主队编号',
  `dtid` int(11) NOT NULL COMMENT '客队编号',
  `jq` int(11) NULL DEFAULT 0 COMMENT '进球',
  `sq` int(11) NULL DEFAULT 0 COMMENT '输球',
  `status` int(11) NULL DEFAULT NULL COMMENT '0:未开赛 1:取消比赛 2:正在比赛 3:比赛结束',
  `mdate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '比赛日期',
  `mtime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '比赛时间',
  `class1` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '分类1(如: 小组赛, 16强等)',
  `class2` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '分类2(分组)',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `mtid`(`mtid`, `dtid`, `mdate`) USING BTREE,
  INDEX `index3`(`mdate`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 47613 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ouodds
-- ----------------------------
DROP TABLE IF EXISTS `ouodds`;
CREATE TABLE `ouodds`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `mid` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '比赛场次',
  `lyid` int(11) NOT NULL COMMENT '博彩公司编号',
  `odds11` float NULL DEFAULT NULL COMMENT '即时欧赔_初_胜',
  `odds12` float NULL DEFAULT NULL COMMENT '即时欧赔_初_平',
  `odds13` float NULL DEFAULT 0 COMMENT '即时欧赔_初_负',
  `odds21` float NULL DEFAULT NULL COMMENT '即时欧赔_终_胜',
  `odds22` float NULL DEFAULT NULL COMMENT '即时欧赔_终_平',
  `odds23` float NULL DEFAULT NULL COMMENT '即时欧赔_终_负',
  `chance11` float NULL DEFAULT NULL COMMENT '即时概率_初_胜',
  `chance12` float NULL DEFAULT NULL COMMENT '即时概率_初_平',
  `chance13` float NULL DEFAULT NULL COMMENT '即时概率_初_负',
  `chance21` float NULL DEFAULT NULL COMMENT '即时概率_终_胜',
  `chance22` float NULL DEFAULT NULL COMMENT '即时概率_终_平',
  `chance23` float NULL DEFAULT NULL COMMENT '即时概率_终_负',
  `retratio1` float NULL DEFAULT NULL COMMENT '返还率_初',
  `retratio2` float NULL DEFAULT NULL COMMENT '返还率_终',
  `kaili11` float NULL DEFAULT NULL COMMENT '即时凯利_初_胜',
  `kaili12` float NULL DEFAULT NULL COMMENT '即时凯利_初_平',
  `kaili13` float NULL DEFAULT NULL COMMENT '即时凯利_初_负',
  `kaili21` float NULL DEFAULT NULL COMMENT '即时凯利_终_胜',
  `kaili22` float NULL DEFAULT NULL COMMENT '即时凯利_终_平',
  `kaili23` float NULL DEFAULT NULL COMMENT '即时凯利_终_负',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `mid`(`mid`, `lyid`) USING BTREE,
  INDEX `mid_2`(`mid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16734719 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for rqodds
-- ----------------------------
DROP TABLE IF EXISTS `rqodds`;
CREATE TABLE `rqodds`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `mid` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '比赛场次',
  `lyid` int(11) NOT NULL COMMENT '博彩公司编号',
  `num` int(11) NOT NULL COMMENT '让球数量',
  `odds11` float NULL DEFAULT NULL COMMENT '即时欧赔_初_胜',
  `odds12` float NULL DEFAULT NULL COMMENT '即时欧赔_初_平',
  `odds13` float NULL DEFAULT 0 COMMENT '即时欧赔_初_负',
  `odds21` float NULL DEFAULT NULL COMMENT '即时欧赔_终_胜',
  `odds22` float NULL DEFAULT NULL COMMENT '即时欧赔_终_平',
  `odds23` float NULL DEFAULT NULL COMMENT '即时欧赔_终_负',
  `chance11` float NULL DEFAULT NULL COMMENT '即时概率_初_胜',
  `chance12` float NULL DEFAULT NULL COMMENT '即时概率_初_平',
  `chance13` float NULL DEFAULT NULL COMMENT '即时概率_初_负',
  `chance21` float NULL DEFAULT NULL COMMENT '即时概率_终_胜',
  `chance22` float NULL DEFAULT NULL COMMENT '即时概率_终_平',
  `chance23` float NULL DEFAULT NULL COMMENT '即时概率_终_负',
  `retratio1` float NULL DEFAULT NULL COMMENT '返还率_初',
  `retratio2` float NULL DEFAULT NULL COMMENT '返还率_终',
  `kaili11` float NULL DEFAULT NULL COMMENT '即时凯利_初_胜',
  `kaili12` float NULL DEFAULT NULL COMMENT '即时凯利_初_平',
  `kaili13` float NULL DEFAULT NULL COMMENT '即时凯利_初_负',
  `kaili21` float NULL DEFAULT NULL COMMENT '即时凯利_终_胜',
  `kaili22` float NULL DEFAULT NULL COMMENT '即时凯利_终_平',
  `kaili23` float NULL DEFAULT NULL COMMENT '即时凯利_终_负',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `mid`(`mid`, `lyid`, `num`) USING BTREE,
  INDEX `mid_2`(`mid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 55400 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for season
-- ----------------------------
DROP TABLE IF EXISTS `season`;
CREATE TABLE `season`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `lsid` bigint(20) NOT NULL COMMENT '联赛编号',
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '赛季名称',
  `bdate` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '起始日期',
  `edate` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '截至日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1197 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sizeodds
-- ----------------------------
DROP TABLE IF EXISTS `sizeodds`;
CREATE TABLE `sizeodds`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `mid` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `lyid` int(11) NOT NULL,
  `myid` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '大小指数编号(一场球赛一个博彩公司)',
  `dtdate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '通过这个时间和myid可以获取明细数据',
  `immodds1` float NULL DEFAULT NULL COMMENT '即时大小_大',
  `immdisc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '即时盘口',
  `immodds2` float NULL DEFAULT NULL COMMENT '即时大小_小',
  `immdate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '变更时间',
  `immstatus` tinyint(4) NOT NULL DEFAULT 1 COMMENT '1表示Odds1赢,2表示Odds1平',
  `initodds1` float NULL DEFAULT NULL COMMENT '初始大小_大',
  `initdisc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '初始盘口',
  `initodds2` float NULL DEFAULT NULL COMMENT '初始大小_小',
  `initdate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '变更时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `mid`(`mid`, `lyid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6929153 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sizeoddsdetail
-- ----------------------------
DROP TABLE IF EXISTS `sizeoddsdetail`;
CREATE TABLE `sizeoddsdetail`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `soid` bigint(20) NOT NULL,
  `odds1` float NULL DEFAULT NULL,
  `disc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `odds2` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `index2`(`soid`, `disc`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1143444 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for yaodds
-- ----------------------------
DROP TABLE IF EXISTS `yaodds`;
CREATE TABLE `yaodds`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `mid` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `lyid` int(11) NOT NULL,
  `myid` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '亚赔编号(一场球赛一个博彩公司)',
  `dtdate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '通过这个时间和myid可以获取明细数据',
  `immodds1` float NULL DEFAULT NULL COMMENT '即时盘口水1',
  `immdisc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '即时盘口',
  `immodds2` float NULL DEFAULT NULL COMMENT '即时盘口水2',
  `immdate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '变更时间',
  `immstatus` tinyint(4) NOT NULL DEFAULT 1 COMMENT '1表示Odds1赢,2表示Odds1平',
  `initodds1` float NULL DEFAULT NULL COMMENT '初始盘口水1',
  `initdisc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '初始盘口',
  `initodds2` float NULL DEFAULT NULL COMMENT '初始盘口水2',
  `initdate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '变更时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `mid`(`mid`, `lyid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4159602 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for yaoddsdetail
-- ----------------------------
DROP TABLE IF EXISTS `yaoddsdetail`;
CREATE TABLE `yaoddsdetail`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `yoid` bigint(20) NOT NULL,
  `odds1` float NULL DEFAULT NULL,
  `disc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `odds2` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `index2`(`yoid`, `disc`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 552207 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
