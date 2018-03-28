create database if not exists zhuhaibus default character set utf8;
use zhuhaibus;

create table feedback (
feedback_id int unsigned not null auto_increment comment '自增主键',
app varchar(16) not null default 'zhbus',
vc varchar(16) not null default '' comment '版本号',
vn varchar(32) not null default '' comment '版本名',
ch varchar(16) not null default '' comment '渠道',
contact varchar(64) not null default '' comment '联系方式',
content varchar(512) not null default '',
create_ts bigint unsigned not null default 0,
primary key (feedback_id)
) engine=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

create table news (
news_id int unsigned not null auto_increment comment '自增主键',
dt char(8) not null default '20180321' comment '日期',
pt varchar(16) not null default '' comment '平台',
origin_id varchar(16) not null default '0' comment '知乎id',
title varchar(64) not null default '',
cover varchar(256) not null default '',
news_ts bigint unsigned not null default 0,
detail text not null,
primary key (news_id)
) engine=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;