$(document).ready(function(){
    $('#start-session').click(function(){
        var input_data = {
            'session_id': $(this).closest('.session').data('session-id')
        };
        $.post("{{ url_for('View:start_session') }}", input_data, function( data ) {
            location.href = "{{ url_for('View:scan_session', session_id=session_id) }}";
        });
    });

    $('#delete-session').click(function(){
        var session_id = $(this).closest('.session').data('session-id')
        // Can't use url_for here because we need session_id on jinja render, which we can't get.
        $.post("/delete-session/" + session_id, {}, function( data ) {
            // todo: don't need to reload the page, just delete the element(card) if it was successful
            location.href = "{{ url_for('View:index') }}";
        });
    });
});