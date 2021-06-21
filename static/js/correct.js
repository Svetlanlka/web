$('.js-correct').click(function(ev) {
    ev.preventDefault();
    var $this = $(this),
        objid = $this.data('objid');

    $.ajax("/change_correct/", {
        method: 'POST',
        data: {
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

        is_correct = '#answer_correct' + objid
        not_correct = '#answer_not_correct' + objid
        check = '#answer_check' + objid
        console.log(is_correct, not_correct)

     
        if (data.is_correct) {
            $(is_correct).css("display", "block");
            $(not_correct).css("display", "none");
            $(check).prop("checked", true);
        } else {
            $(is_correct).css("display", "none");
            $(not_correct).css("display", "block");
            $(check).prop("checked", false);
        }

    });
    
    console.log("CLICK: " + "answer " + objid);
});