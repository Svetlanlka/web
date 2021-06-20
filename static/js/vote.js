$('.js-vote').click(function(ev) {
    ev.preventDefault();
    var $this = $(this),
        action = $this.data('action'),
        objid = $this.data('objid');
        href = $this.data('href')
    let url = ''
    if (href == 'question') {
        url = '/questions/' + objid + '/vote/';
    } else if (href == 'answer') {
        url = '/answer_vote/';
    }
    $.ajax(url, {
        method: 'POST',
        data: {
            action: action,
            obj_id: objid,
        },
    }).done(function(data) {
        console.log("RESPONSE: ", data);

        if (data.not_login) {
            if (window.location.search === '') {
                window.location = window.location.origin + '/login/?next=' + window.location.pathname;
            } else {
                window.location = window.location.origin + '/login/' + window.location.search + '?next=' + window.location.pathname;
            }
        }
        
        v  = data.vote
        is_like = '#' + href + '_like' + objid
        not_like = '#' + href + '_not_like' + objid
        is_dislike = '#' + href + '_dislike' + objid
        not_dislike = '#' + href + '_not_dislike' + objid
        console.log(is_like + " " + not_like + " " + is_dislike + " " + not_dislike)
     
        if (v == '0') {
            $(not_dislike).css('display', "block");
            $(is_dislike).css('display', 'none');
            $(is_like).css("display", "none");
            $(not_like).css("display", "block");
        }
        if (v == '1') {
            $(is_like).css("display", "block");
            $(not_like).css("display", "none");
            $(is_dislike).css('display', "none");
            $(not_dislike).css('display', 'block');
        }
        if (v == '-1') {
            $(is_like).css("display", "none");
            $(not_like).css("display", "block");
            $(is_dislike).css('display', "block");
            $(not_dislike).css('display', 'none');
        }
        new_rating = '#' + href + "_rating" + objid
        if (data.vote_rating < 0) $(new_rating).text('0');
        else $(new_rating).text(data.vote_rating);
        console.log(new_rating)
    });
    
    console.log("CLICK: " + href + " " + action + " " + objid);
});