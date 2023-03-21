  var loadFile = function(event) {
  var output = document.getElementById('output');
  output.src = URL.createObjectURL(event.target.files[0]);
  output.onload = function() {
    URL.revokeObjectURL(output.src) // free memory
  }
  $('#editImage').css('margin-left', '0');
  $('#editImage').css('width', '50%');
  $('#editImage').css('float', 'left');
  $('#output').css('margin-right', '0');
  $('#output').css('width', '50%');
  $('#output').css('float', 'right');
  $('#changedoutput').show();
  $('#editimgname').hide();
  $('#buttonbox').css('width', '100%');
  $('#canceleditbutton').css('float', 'left');
  $('#canceleditbutton').css('width', '50%');
  $('#canceleditbutton').css('margin-left', 'auto');
  $('#canceleditbutton').css('margin-right', 'auto');
  $('#confirmbutton').css('float', 'right');
  $('#confirmbutton').css('width', '50%');
  $('#confirmbutton').css('margin-left', 'auto');
  $('#confirmbutton').css('margin-right', 'auto');

  $("#canceleditbutton").on("click", function(){
    $('#changedoutput').hide();
    $('#editimgname').show();
    $('#editImage').css('margin-left', 'auto');
    $('#editImage').css('width', '75%');
    $('#editImage').css('float', 'None');
    $("#fileinputofimage").val(null);
    $("#fileinputofimage").val('');
  });

  $("#confirmbutton").on("click", function(){
    $('#editImage').hide();
    $('#output').css('width', '75%');
    $('#output').css('margin-right', 'auto');
    $('#output').css('margin-left', 'auto');
    $('#output').css('display', 'block');
    $('#output').css('float', 'None');
    $('#canceleditbutton').hide();
    $('#confirmbutton').hide();
  });
};



//$("[type=file]").on("change", function(){
    // Name of file and placeholder
//    var file = this.files[0].name;
//    var dflt = $(this).attr("placeholder");
//    if($(this).val()!=""){
//      $(this).next().text(file);
//     } else {
//       $(this).next().text(dflt);
//     }
//   });

//   if ($('#File').get(0).files[0].size === 0) {
//     window.alert("missing file");
// }

