#coding=utf8
create table person_court_info(
    id integer primary key autoincrement,
    case_id text comment '�����������',
    iname text comment '��ִ��������/����',
    sexy text comment '�Ա�',
    age TINYINT comment '����',
    cardNum text comment '���֤����/��֯��������',
    courtName text comment 'ִ�з�Ժ',
    areaName text comment 'ʡ��',
    gistId text comment 'ִ�������ĺ�',
    regDate text comment '����ʱ��',
    caseCode text comment '����',
    gistUnit text comment '����ִ�����ݵ�λ',
    duty text comment '��Ч��������ȷ��������',
    performance text comment '��ִ���˵��������',
	performedPart text comment '�Ѿ����в���',
	unperformPart text comment 'δ���в���',
    disruptTypeName text comment 'ʧ�ű�ִ������Ϊ��������',
    publishDate text comment '����ʱ��',
    partyTypeName integer comment '��ע����',
    remark text comment '��ע'
    );