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

TAG_CID_URL = '/j/tag/'
function tag_cid_page(cid, page){
    var tag_cid = $('#tag_cid_page'+cid).html('<div class="readloading"></div>'),
    item_list_cid = $('#item_list_'+cid),
    com_main_cid = '#com_main_'+cid;

    $.get(TAG_CID_URL+cid+'-'+page,function(data){


        if(page>0){
            item_list_cid.html('')
        }
        _render_note(com_main_cid,'#item_list_'+cid, data.li);
        var p=data.page
        if(!p){
            tag_cid.css('border',0)
        };
        tag_cid.html(p||'')
        if(page>0){
            $(window).scrollTop($(com_main_cid).offset().top-6);
        }
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
            '<a class="TPH read_author" href="${link}" target="_blank">${user_name}</a>'+
            '{{else}}'+
            '<span class="read_author">银河系</span>'+
            '{{/if}}'+
        '</div>'+
    '</pre>'+
    '<div class="fdbar">'+
        '<a href="javascript:void(0)" class="readx" title="快捷键 ESC"></a>'+
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
);

(function(){
var READPAD_NAV;
function readpad_nav_resize(){
    if(READPAD_NAV){
        READPAD_NAV.width(READPAD_NAV[0].parentNode.offsetWidth-2)
    }
};
$(window).resize(readpad_nav_resize);

$.template(
    'po_tag_list',
    '<input type="hidden" id="tag_search" /><a class="tag_edit_btn" href="javascript:void(0)">完成</a>'+
    '<span class="po_tag_list">'+
        '{{each tag_list}}'+
            '<a class="po_tagw" target="_blank" href="http://${$value[1]}${HOST_SUFFIX}"><span class="po_tag_pic"></span><span class="po_tag_one" >${$value[0]}</span></a>'+
        '{{/each}}'+
    '{{if tag_list.length}}'+
       '<a class="tag_list_edit_a" href="javascript:void(0)">编辑</a>'+
    '{{else}}'+
        '<a class="tag_list_edit_a tag_list_add_a" href="javascript:void(0)">添加标签</a>'+
    '{{/if}}'+
    '</a></span>'
);


note_li = function (feed_index, result){
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
            '<span id="readtag"></span>'+
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
        txt_body,
        readtag = txt_loading.find("#readtag");

            //'<input id="search" type="hidden">'+
            /*
    function close_token(){
        if($('.po_tag_list')[0])$('.po_tag_list').remove()
        if($('.tag_edit_btn')[0])$('.tag_edit_btn').remove()
        $('.main_nav').find('ul.token-input-list').remove()           
    }*/


    function readx(){
        if(oldtop<0)return;
        txt_loading.remove()
        feeds.show()
        //feed_index.show()
        //$('.com_main').show()
        txt_body.replaceWith(read_loading)
//console.info(oldtop)
        winj.scrollTop(oldtop)
        oldtop=-1
    }


    $(document).bind("keyup",function(e){
        if(e.keyCode == 27&&!$("#fancybox-wrap").is(':visible')){
            readx()
        }
    })
    $('.readx').live('click', readx)


    result.find('.reada').click(function(){

        READPAD_NAV = txt_loading.find('#main_nav_txt');
        oldtop=winj.scrollTop();

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
//console.info(oldtop)
        winj.scrollTop(scrollTop);
        readtag.html( '')

        $.get(
        "/j/po/json/"+id,
        function(r){
            r.id=id
            /*
            if(user[0]){
                user_link=user[0].href+id
            }else{
                user_link = 0
            }
            */
            //r.user_name=user.html()
            //r.link = user_link

            r.time = $.timeago(r.create_time)
            r.fav = $('#fav'+id)[0].className
            readtag.html( $.tmpl('po_tag_list',r))
            txt_body = $.tmpl('note_txt',r)
            read_loading.replaceWith(txt_body)
            txt_title.html(title.html())
            var fdopt = txt_body.find('.fdopt'),
                readauthor = txt_body.find('.readauthor')
            txt_opt.html(fdopt.html())
            fdopt.replaceWith(readauthor.html())
            readauthor.remove()

           var tags = r
           function _(){
                $('.po_tag_list').remove()
                $('.tag_edit_btn').show().css('display','inline-block').click(function(){
                    var tag_id_list=[]
                    $("input[name='tag_id_list']").each(function(){
                        tag_id_list.push($(this).val())
                    })
                    $.postJSON(
                        '/j/tag/po/'+id,
                        {tag_id_list:$.toJSON(tag_id_list)},
                        function(data){
                            readtag.html(
                                $.tmpl('po_tag_list',data)
                            )
                            tags = data
                            $('.tag_list_edit_a').click(_)
                            //close_token()
                        }
                    )
                })
                autocomplete_tag('#tag_search', tags.tag_list||[],'tag')
            }
            $('.tag_list_edit_a').click(_)
            winj.scrollTop(scrollTop)
            readpad_nav_resize()
            scroll_to_fixed(READPAD_NAV,8,{position:'fixed',"top":0},{position:'absolute',marginTop:0})

        })

        return false; 
    })



/*            var nav_txt =$('#main_nav_txt'), do_width = function(){
                nav_txt.css('width',$('.readpad').width())
            }
            do_width()
            nav_txt.resize(do_width)
*/
};


})();
