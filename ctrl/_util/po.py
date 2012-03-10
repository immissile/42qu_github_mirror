#coding:utf-8
from model.po_pic import pic_list, mc_pic_id_list


def update_pic(form, user_id, po_id, id):
    pl = pic_list(user_id, id)
    for pic in pl:
        seq = pic.seq

        title = 'tit%s' % seq
        if title in form:
            title = form[title][0]
        else:
            title = ''

        align = 'pos%s' % seq
        if align in form:
            align = int(form[align][0])
            if align not in (-1, 0, 1):
                align = 0
        else:
            align = 0

        pic.title = title.strip()
        align = int(align)


        pic.align = align
        pic.po_id = po_id
        pic.save()

    mc_pic_id_list.delete(
        '%s_%s' % (user_id, id)
    )

if __name__ == "__main__":
    pass



