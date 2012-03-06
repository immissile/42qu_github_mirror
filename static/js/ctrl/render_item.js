$.template(
    'note_li',
    '<div class="readl c">'+
        '<div id="reado${$data[0]}" class="reado">'+
            '<a rel="${$data[0]}" href="javascript:void(0)" id="fav${$data[0]}" class="fav${$data[0]} fav{{if $data[5]}}ed{{/if}}"></a>'+
            '<span class="reada">'+
                '<span class="title">${$data[1]}</span>'+
                '<span class="rtip">${$data[2]}</span>'+
            '</span>'+
        '</div>'+
        '{{if $data[3]}}<div class="zname">'+
            '<a href="#" rel="${$data[3]}" class="TPH" target="_blank">${$data[4]}</a>'+
        '</div>{{/if}}'+
    '</div>'
)


$.template(
    'tag_cid',
'<div class="com_main" id="com_main_${$data[0]}">'+
    '<div id="feeds"><div id="feed_index">'+
        '<div class="main_nav">'+
            '<span class="now">'+
                '${$data[1]}'+
            '</span>'+
            '<span class="R">共 ${$data[2]} 篇</span>'+
        '</div>'+
        '<div id="item_list_${$data[0]}" class="tag_item_list"></div>'+
        '{{if $data[4]}}<div class="tag_cid_page" id="tag_cid_page${$data[0]}">'+
            '<a class="more" href="javascript:tag_cid_page(${$data[0]},-${$data[4]})">更多 ...</a>'+
        '</div>{{/if}}'+
    '</div></div>'+
'</div>'
)

function tag_cid_page(cid, page){
    var tag_cid = $('#tag_cid_page'+cid).html('<div class="readloading"></div>'),
    item_list_cid = $('#item_list_'+cid);

    $.get('/j/tag/'+cid+'-'+page,function(data){


        if(page>0){
            item_list_cid.html('')
        }
        _render_note('#com_main_'+cid,'#item_list_'+cid, data.li);
        var p=data.page
        if(!p){
            tag_cid.css('border',0)
        };
        tag_cid.html(p||'')

    })
}

function _render_tag_cid(id, data){
    $.tmpl('tag_cid', data).appendTo(id)
    var i=0,cid, item, t;
    for(;i<data.length;++i){
        t = data[i]
        cid = t[0]
        item = t[3]
        _render_note("#com_main_"+cid, "#item_list_"+cid, item)
    }
}

function _render_note(feed_index, elem, data){
    var result = $.tmpl('note_li', data)
    result.find('.TPH').each(function(){
        this.href="//"+this.rel+HOST_SUFFIX
    })
    result.appendTo(elem);
    note_li($(feed_index), result)
    return result
}


$.template(
    'note_txt',
    '<pre class="prebody">{{html txt}}'+
        '<div class="readauthor">'+
            '来自'+
            '{{if link}}'+
            '<a class="aH read_author" href="${link}" target="_blank">{{html user_name}}</a>'+
            '{{else}}'+
            '<span class="read_author">银河系</span>'+
            '{{/if}}'+
        '</div>'+
    '</pre>'+
    '<div class="fdbar">'+
        '<a href="javascript:void(0)" class="readx"></a>'+
        '<span><span class="fdopt">'+
            '<a class="${fav} fav${id}" href="javascript:void(0)" rel="${id}"></a>'+
                '<span class="split">-</span>'+
            '<a href="javascript:share(${id});void(0)" class="vote">推荐</a>'+
                '<span class="split">-</span>'+
            '<a href="/po/${id}" target="_blank" class="fcma bzreply">'+
                '<span class="count mr3">{{if reply_count}}${reply_count}{{/if}}</span>'+
                '评论'+
            '</a>'+
        '</span></span>'+
    '</div>'
)
var READX;

function note_li(feed_index, result){
    var feeds=$(feed_index[0].parentNode), 
        scrollTop,
        oldtop=-1,
        winj=$(window),
        txt_loading=$(
'<div class="readpad">'+
    '<div class="main_nav" id="main_nav_txt">'+
        '<div id="main_nav_in">'+
            '<div id="main_nav_opt"></div>'+
            '<a href="javascript:void(0)" title="快捷键 ESC" class="readx"></a>'+
        '</div>'+
    '</div>'+
    '<div id="main_nav_title" class="readtitle"></div>'+
    '<div id="read_loading"></div>'+
'</div>'
        ),
        txt_title=txt_loading.find('#main_nav_title'),
        main_nav_txt=txt_loading.find('#main_nav_txt'),
        read_loading=txt_loading.find('#read_loading'),
        txt_opt=txt_loading.find('#main_nav_opt'),
        txt_body;

    function readx(noscroll){
        if(oldtop<0)return;
        txt_loading.remove()
        feeds.show()
        //feed_index.show()
        //$('.com_main').show()
        if(!noscroll){ 
            winj.scrollTop(oldtop)
        }
        oldtop=-1
        txt_body.replaceWith(read_loading)
    }


    $(document).bind("keyup",function(e){
        if(e.keyCode == 27){
            READX()
        }
    })
    $('.readx').live('click', function(){READX()})

    READX = readx

    result.find('.reada').click(function(){
        if(READX){
            READX(1)
        }
        READX = readx

        scrollTop = feeds.offset().top-14
        feeds.hide()
        //feed_index.hide();
        //$('.com_main').hide()
        var p = this.parentNode,
            self=$(p), 
            title=self.find('.title').addClass('c9'), 
            id=p.id.slice(5), 
            user=$(p.parentNode).find('.TPH'),
            user_link
            ;
        //feeds.append(txt_loading);
        feeds.after(txt_loading)
        oldtop=winj.scrollTop();
        winj.scrollTop(scrollTop);
        txt_title.html(title.html())
        var style1 = {'position':'fixed',"top":0},style2 = {'position':'absolute',"marginTop":0}
        scroll_to_fixed('#main_nav_txt',8,style1,style2)


        $.get(
        "/j/po/json/"+id,
        function(r){
            r.id=id
            if(user[0]){
                user_link=user[0].href+id
            }else{
                user_link = 0
            }
            r.user_name=user.html()
            r.link = user_link
            r.time = $.timeago(r.create_time)
            r.fav = $('#fav'+id)[0].className
            txt_body = $.tmpl('note_txt',r)
            read_loading.replaceWith(txt_body)
            var fdopt = txt_body.find('.fdopt'),
                readauthor = txt_body.find('.readauthor')
            txt_opt.html(fdopt.html())
            fdopt.replaceWith(readauthor.html())
            readauthor.remove()
            winj.scrollTop(scrollTop)
        })

        return false; 
    })




};



