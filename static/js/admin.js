const btnDelete= document.querySelectorAll('.btn-delete');
if(btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        if(!confirm('Are you sure you want to delete it?')){
        e.preventDefault();
        }
    });
    })
}

var loadFile = function(event) {
var output = document.getElementById('uploadimg');
output.src = URL.createObjectURL(event.target.files[0]);
output.onload = function() {
    URL.revokeObjectURL(output.src) // free memory
}
    $('#uploadimg').css('margin-left', 'auto');
    $('#uploadimg').css('margin-right', 'auto');
    $('#uploadimg').css('width', '75%');
    $('#uploadimg').css('display', 'block');
    $('#uploadimg').show();

};
  
$(document).ready(function(){
    $('.modal').on('hidden.bs.modal', function () {
        $(this).find('form').trigger('reset');
    });
    $('#addModal').on('hidden.bs.modal', function () {
        $('#uploadimg').hide();
    });
});
  

$(document).ready(function() {
    var now     = new Date(); 
    var year    = now.getFullYear();
    var month   = now.getMonth()+1; 
    var day     = now.getDate();
    var hour    = now.getHours();
    var minute  = now.getMinutes();
    var second  = now.getSeconds(); 
    if(month.toString().length == 1) {
         month = '0'+month;
    }
    if(day.toString().length == 1) {
         day = '0'+day;
    }   
    if(hour.toString().length == 1) {
         hour = '0'+hour;
    }
    if(minute.toString().length == 1) {
         minute = '0'+minute;
    }
    if(second.toString().length == 1) {
         second = '0'+second;
    }   
    var dateTime = year+'/'+month+'/'+day+' '+hour+'_'+minute+'_'+second;   
    $('#medtable').DataTable({   
        responsive: true,  
        dom:"<'row'<'col-md-6'l><'col-md-6'f>>" +
        "<'row'<'col-md-12'B>>" +
        "<'row'<'col-md-12'tr>>" +
        "<'row'<'col-md-5'i><'col-md-7'p>>",
        buttons: [
            {
                extend: 'excel',
                exportOptions: {
                    columns: [0,1,3,4,5,6,7,8]
                },
                filename: function () {
                    return 'PERMELIS Database - ' + dateTime;
            }
        },
            {
                extend: 'csv',
                exportOptions: {
                    columns: [0,1,3,4,5,6,7,8]
                },
                filename: function () {
                    return 'PERMELIS Database - ' + dateTime;
                }
            }],
        "order": [[ 1, "asc" ]],
        "aLengthMenu": [[3, 5, 10, 25, -1], [3, 5, 10, 25, "All"]],
        "iDisplayLength": 5
        });
} );
    