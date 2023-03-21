$(document).ready(function(){
    $('.publicationname').click(function(){
        var id = $(this).data('id');
        $.ajax({
            url: '/ajaxfile',
            type: 'post',
            data: {id: id},
            success: function(data){ 
                $('#empModal .modal-body').html(data); 
                $('#empModal .modal-body').append(data.htmlresponse);
                $('#empModal').modal('show'); 
                $("#empModal").css("z-index", "1500000");
            }
        });
    });
});

$(document).ready(function(){
    $('.publicationimage').click(function(){
        var id = $(this).data('id');
        $.ajax({
            url: '/ajaxfile',
            type: 'post',
            data: {id: id},
            success: function(data){ 
                $('#empModal .modal-body').html(data); 
                $('#empModal .modal-body').append(data.htmlresponse);
                $('#empModal').modal('show'); 
                $("#empModal").css("z-index", "1500000");
            }
        });
    });
});

$(document).ready(function(){
    $('.addbutton').click(function(){
        var id = $(this).data('id');
        $.ajax({
            url: '/add',
            type: 'post',
            data: {id: id},
            success: function(data){ 
                $('#cartresult').html(data); 
                $('#cartresult').append(data.htmlresponse);
                $('.cartremark').hide();
                }
        });
    });
});

$(document).ready(function(){
    $('.addbutton').click(function(){
        $(".alert-box").fadeIn(300).delay(1500).fadeOut(400);
    });
})
