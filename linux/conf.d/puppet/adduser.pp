define adduser($uid,$groups) {
    user { 
        "$name":
             uid => $uid,
             home => "/home/$name",
             shell => "/bin/bash",
	     password => "42qu";
    }
    file {
	 "/home/$name":
	   owner   => $uid,
	   mode    => 750,
	   ensure  => directory;
    }
    file {
         "/home/$name/.ssh":
	   owner   => $uid,
	   group   => $uid,
	   mode    => 700,
	   ensure  => directory,
	   require => File["/home/$name"];
    }
}

