$(function() {
    $("#search_button").click(function() {
        var search_word = $("#search_box").val();
        var dataString = 'search_word='+ search_word;
        var searchLength = search_word.length;
        if(searchLength<2){
          $('#search_box').popover('show');
          $('#lengthcomment').show();
        }else{
          $('#search_box').popover('hide');
          $('#lengthcomment').hide();
          $.ajax({
            type: "POST",
            url: "/fetchrecords",
            data: dataString,
            cache: false,
            beforeSend: function(html) {
                document.getElementById("result").innerHTML = ''; 
                $("#flash").show();
                $("#flash").html('<img src="/static/icons/loader.gif"> Loading Results...');
              },
            success: function(html){
                $("#result").show();
                $("#result").append(html.data);
                $("#flash").hide();
            }
          });
        }
      return false;
    });
  });

