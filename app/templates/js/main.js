$(document).ready(function(){

    $('#create-session').click(function(){
        // clear the ID, name, and description fields for new entries
        $('#session_id_field').val('');
        $('#form_name_field').val('');
        $('#form_description_field').val('');
    });

    $('.edit-session').click(function(){
        // set ID
        var session_id = $(this).data('session-id');
        $('#session_id_field').val(session_id);

        // set Name
        var form_name = $(this).data('name');
        $('#form_name_field').val(form_name);

        // set Description
        var form_description = $(this).data('description');
        $('#form_description_field').val(form_description);
    });

    $('.delete-session').click(function(){
        // set ID
        var session_id = $(this).data('session-id');
        $('#delete_session_id_field').val(session_id);
    });

    // todo: i'm keeping this here in case we need it later
    // $('.delete-session').click(function(){
    //     var session_id = $(this).closest('.session').data('session-id');
    //     // Can't use url_for here because we need session_id on jinja render, which we can't get.
    //     $.post("/delete-session/" + session_id, {}, function( data ) {
    //         // todo: don't need to reload the page, just delete the element(card) if it was successful
    //         location.href = "{{ url_for('View:index') }}";
    //     });
    // });

    // initiate tooltips
    $('[data-toggle="tooltip"]').tooltip();
});