truncate zpage.user_mail;
insert into zpage.user_mail (user_id, mail)
select man_id, mail from qu.man_mail where man_id > 0 order by id;

truncate zpage.user_password;
insert into zpage.user_password (id, password)
select id, password from qu.man_password order by id;

truncate zpage.url;
insert into zpage.url (id, url)
select id, url from qu.man where url > '' order by id;

truncate zpage.user_session;
insert into zpage.user_session (id, value)
select id, ck from qu.man_session order by id;

truncate zpage.zsite;
insert into zpage.zsite (id, name, cid, state)
select id, name, cid, state from qu.man order by id;

truncate zpage.pic;
insert into zpage.pic (id, zsite_id, tid)
select id, man_id, 2 from qu.pic order by id;

truncate zpage.ico;
insert into zpage.ico (id, value)
select man_id, pic_id from qu.pic_show order by id desc
on duplicate key update value=value;
