/* ONLINE TABLES */
/* userdata table */
create table userdata(username text primary key not null, passhash text not null, fullname text not null, emailadr text not null, digisign text not null, pubkeynn text not null, pubkeyee text not null)

/* grupinfo table */
create table grupinfo(grupiden text primary key not null, grupname text not null, ownrname text not null, foreign key(username) references userdata(username))

/* grupteam table */
create table grupteam(useriden text primary key not null, grupiden text not null, username text not null, foreign key(username) references userdata(username), foreign key(grupiden) references grupinfo(grupiden))

/* sendotoo table */
create table sendotoo(mailiden text primary key not null, subjtext text not null, conttext text not null, srceuser text not null, destuser text not null, timestmp text not null, isitrmov text not null, foreign key(srceuser) references userdata(username), foreign key(destuser) references userdata(username))

/* sendotom table */
create table sendontm(mailiden text primary key not null, subjtext text not null, conttext text not null, srceuser text not null, destlist text not null, timestmp text not null, isitrmov text not null, foreign key(srceuser) references userdata(username))

/* grupmail table */
create table grupmail(mailiden text primary key not null, grupiden text not null, subjtext text not null, conttext text not null, srceuser text not null, timestmp text not null, isitrmov text not null, foreign key(grupiden) references grupinfo(grupiden), foreign key(srceuser) references userdata(username))

/* contacts table */
create table contacts(listiden text primary key not null, ownrname text not null, usercont text not null, foreign key(ownrname) references userdata(username), foreign key(usercont) references userdata(username))

/* recvotoo table */
create table recvotoo(mailiden text primary key not null, subjtext text not null, conttext text not null, srceuser text not null, destuser text not null, timestmp text not null, isitrmov text not null, foreign key(srceuser) references userdata(username), foreign key(destuser) references userdata(username))

/* recvontm table */
create table recvontm(mailiden text primary key not null, subjtext text not null, conttext text not null, srceuser text not null, destlist text not null, timestmp text not null, isitrmov text not null, foreign key(srceuser) references userdata(username))

/* sessdata table */
create table sessdata(sessiden text primary key not null, username text not null, strttime text not null, stoptime text not null, foreign key(username) references userdata(username))

/* OFFLINE TABLES */
/* settings table */
create table settings(username text primary key not null, pkcsiden text not null, pubkeynn text not null, pubkeyee text not null, prvkeynn text not null, prvkeyee text not null, prvkeydd text not null, prvkeypp text not null, prvkeyqq text not null)

/* sessdata table */
create table sessdata(sessiden text primary key not null, username text not null, strttime text not null, stoptime text not null)
