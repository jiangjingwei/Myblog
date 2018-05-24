$(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFtoken', $.cookie('csrftoken'))
        }
    });

    // 点赞
    $('.vote-up').click(function () {
        var $user = $('#user-id');
        if($user.text()){
            var article_id = $(this).attr('article');
            var user_id = $user.attr('userid');
            var $vote = $(this);
            $.ajax({
                url:'/vote_up/',
                type:'POST',
                data:{'article_id':article_id, 'user_id':user_id},
                success:function (data) {
                    if(data['vote_status']){
                        $vote.addClass('vote-active');
                    }else {
                        alert(data['error_msg'])
                    }

                }
            })
        }else {
            alert(location.pathname);
            alert(location.href)
        }

    });

    // 踩灭
    $('.vote-down').click(function () {
        alert('不能踩灭此文章')
    });
    
    // 生成树级评论
    function treeComments(data) {

        var html = '';
        $.each(data,function (k,v) {
            // var $li = $('<li class="am-comment">');
            // var $a = $('<a>').append($('<img src="static/images/default.jpg" alt="" class="am-comment-avatar" width="48" height="48">'));
            // var $main = $('<div class="am-comment-main">').append();
            // console.log(k,v);
            var comment_str = '<li class="am-comment">\n' +
                '                    <a href="#">\n' +
                '                        <img src="/static/images/default.jpg" alt="" class="am-comment-avatar" width="48" height="48">\n' +
                '                    </a>\n' +
                '                    <div class="am-comment-main">\n' +
                '                        <header class="am-comment-hd">\n' +
                '                            <div class="am-comment-meta">\n' +
                '                                <a href="am-comment-author">'+ v["user_id"] + '</a>\n' +
                '                                评论于\n' +
                '                                <time datetime="2013-07-27T04:54:29-07:00">'+ v["create_time"] +'</time>\n' +
                '                            </div>\n' +
                '                        </header>\n' +
                '                        <div class="am-comment-bd">\n' +
                '                            <p>'+ v["content"] +'</p>\n' +
                '                        </div>\n' +
                '                        <footer class="am-comment-footer">\n' +
                '                            <div class="am-comment-actions">\n' +
                '                                <a href=""><i class="am-icon-thumbs-up"></i></a>\n' +
                '                                <a href=""><i class="am-icon-thumbs-down"></i></a>\n' +
                '                                <a href=""><i class="am-icon-reply"></i></a>\n' +
                '                            </div>\n' +
                '                        </footer>\n' +
                '                    </div>\n' +
                '                </li>';

            if(v['children_comment']){
                var children_str = treeComments(v['children_comment']);
                // var str = '@'+ v['parent_comment'] + ' ' + v['content'];
                // children_str.replace(/^<p>.*<\/p>$/, str);
                // console.log(children_str);
                comment_str += children_str
            }

            html += comment_str

        });

        return html


    };

    // 获取此篇文章所有的评论
    if(location.href.match('articleDetail')){
        $.ajax({
            type:'GET',
            success:function (data) {

                var html = treeComments(data);
                $("#am-comments-list").append(html)

            }
        })
    }


});