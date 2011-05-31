cron { logrotate:
    command => "/usr/sbin/ntpdate 3.gentoo.pool.ntp.org > /dev/null;/sbin/hwclock -w",
    user => root,
    hour => 2,
    minute => 0
}
