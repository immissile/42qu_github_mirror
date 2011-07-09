-- change gid
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
select id, name, cid, state from qu.man where qu.man.cid=1 order by id;

truncate zpage.gid;
insert into zpage.gid (id)
select id from qu.man where cid=1 order by id;

truncate zpage.pic;
insert into zpage.pic (id, user_id, cid)
select id, man_id, 2 from qu.pic order by id;

truncate zpage.ico;
insert into zpage.ico (id, value)
select man_id, pic_id from qu.pic_show order by id
on duplicate key update value=values(value);

truncate zpage.ico_pos;
insert into zpage.ico_pos (id, value)
select pic_show.man_id, pic_show_pos.txt from qu.pic_show, qu.pic_show_pos where pic_show.pic_id = pic_show_pos.id order by pic_show.id
on duplicate key update value=values(value);

-- truncate zpage.namecard;
-- insert into zpage.namecard (user_id, pid, phone, mail, address, state)
-- select id, pid, phone, mail, address, 10 from qu.namecard order by id;

truncate zpage.motto;
insert into zpage.motto (id, value)
select id, title from qu.man_title where title > '' order by id;
