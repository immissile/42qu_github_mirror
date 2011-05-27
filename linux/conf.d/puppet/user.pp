import "adduser.pp"

group {
"zpage":
	gid=>1999;
}

adduser{work:uid=>2000,groups=>['zpage']}
adduser{zuroc:uid=>2001,groups=>['zpage']}
adduser{yup:uid=>2002,groups=>['zpage']}
adduser{zjd:uid=>2003,groups=>['zpage']}

