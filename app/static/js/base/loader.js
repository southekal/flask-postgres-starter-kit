$(function() {
    var loader = '<span style="display: none;" id="loadingData"> \
                <img class="mx-auto d-block" src="https://s3.amazonaws.com/zipthunder-images/loading-data.gif"> \
                </span>'

    var $div = $( loader ).prependTo('body');

    $(document).on('click', '.showLoader', function(){
        $( "body" ).css('background-color', "#f2f2f2");
        $( "body" ).css("opacity", "0.5");
        $( "#loadingData" ).show();
     });

})