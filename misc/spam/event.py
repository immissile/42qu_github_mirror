import _env


    rendermail(
        '/mail/buzz/follow_new.htm', mail, name,
        from_user=from_user,
        format='html',
        subject='%s ( %s ) 关注 你' % (
            from_user.name,
            ' , '.join(career),
        )
    )
