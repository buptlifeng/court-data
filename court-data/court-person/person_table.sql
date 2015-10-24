#coding=utf8
drop table if exists person_court_info;
CREATE TABLE person_court_info(
    id integer primary key autoincrement,
    case_id text comment '案件索引编号',
    iname text comment '被执行人姓名/名称',
    sexy text comment '性别',
    age TINYINT comment '年龄',
    cardNum text comment '身份证号码/组织机构代码',
    courtName text comment '执行法院',
    areaName text comment '省份',
    gistId text comment '执行依据文号',
    regDate text comment '立案时间',
    caseCode text comment '案号',
    gistUnit text comment '作出执行依据单位',
    duty text comment '生效法律文书确定的义务',
    performance text comment '被执行人的履行情况',
    performedPart text comment '已经履行部分',
    unperformPart text comment '未履行部分',
    disruptTypeName text comment '失信被执行人行为具体情形',
    publishDate text comment '发布时间',
    partyTypeName integer comment '关注次数',
    remark text comment '备注'
)engine=innodb default charset=utf8;