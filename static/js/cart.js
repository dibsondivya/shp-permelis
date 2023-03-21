$(document).ready(function() {
    // Remove from cart
    $('#carttable').on('click', '#emptyButton', function(){
        $(this).closest('tr').remove();
        if ($('#carttable tbody tr').length == 0){
            $('.cartremark').show();
            $('.content').hide();
        }else{
            $('.cartremark').hide();
        }
    });
    $('.emptyButton').click(function(){
        var id = $(this).data('id');
        $.ajax({
            url: '/empty',
            type: 'post',
            data: {id: id},
            success: function(newremark){ 
                $('#deleteremark').show();
                $('#deleteremark').html(newremark);
                $('#deleteremark').fadeOut(1500); 
                }
        });
    });
    $('.emptyallButton').click(function(){
        $('#carttable tbody tr').length == 0;
        $('.cartremark').show();
        $('.content').hide();
        $.ajax({
            url: '/emptyall',
            type: 'post',
            success: function(newremark){ 
                $('#deleteremark').show();
                $('#deleteremark').html(newremark);
                $('#deleteremark').fadeOut(1500); 
                }
        });
    });
});
