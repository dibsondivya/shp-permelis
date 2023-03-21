$(document).ready(function(){
    $('#simple_form input').jqBootstrapValidation({
        preventSubmit: true,
        submitSuccess: function($form, event){     
            event.preventDefault();
            $this = $('#send_button');
            $this.prop('disabled', true);
            var form_data = $("#simple_form").serialize();
            $.ajax({
               url:"/loginsubmit",
               method:"POST",
               data:form_data,
               success:function(){
                $('#success').html("<div class='alert alert-success'><strong>Successfully Register. </strong></div>");
                $('#simple_form').trigger('reset');
               },
               error:function(){
                $('#success').html("<div class='alert alert-danger'>There is some error</div>");
                $('#simple_form').trigger('reset');
               },
               complete:function(){
                setTimeout(function(){
                 $this.prop("disabled", false);
                 $('#success').html('');
                }, 5000);
               }
            });
        },
    });
 
});
