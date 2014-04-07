$(document ).on('pageinit', function() {
    $('#user_add').on('filterablebeforefilter', function (e, data) {
        var $ul = $(this),
            $input = $(data.input),
            value = $input.val(),
            html = "";
        $ul.html("");
        if (value && value.length > 0) {
            $ul.html('<li><div class="ui-loader"><span class="ui-icon ui-icon-loading"></span></div></li>');
            $ul.listview('refresh');
            $.ajax({
                url: '/users/search/',
                dataType: 'json',
                crossDomain: false,
                data: {
                    q: $input.val()
                }
            })
            .then(function(response) {
                $.each(response, function(i, user) {
                    html += '<li><a href=""><img src="' + user[3] + '" alt="' + user[1]+ '" /><h3>' + user[1] + '</h3><p>' + user[2] + '</p></a><a href="add/' + user[0] + '/" data-ajax="false">Add</a></li>';
                });
                $ul.html(html);
                $ul.listview('refresh');
                $ul.trigger('updatelayout');
            });
        }
    });
});
