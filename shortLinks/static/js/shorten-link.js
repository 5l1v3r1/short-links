$(function () {

  // Get CSRF token from hidden input in form
  let csrftoken = $("[name=csrfmiddlewaretoken]").val();

  /* Functions */

  let copyLink = function () {
    let copyText = $("#id_origin_link");
    copyText.select();
    document.execCommand("copy");
    $("#shortenButton").show();
    $("#copyButton").hide();
  };

  let csrfSafeMethod = function (method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  };

  let postOriginUrl = function (event) {

    /* stop form from submitting normally */
    event.preventDefault();

    /* get the action attribute from the <form action=""> element */
    let form = $("#urlForm");

    $.ajax({
      url: form.attr("action"),
      type: form.attr("method"),
      data: form.serialize(),
      success: function (data) {
        if (data.error) {
          alert('Invalid url!');
        } else {
          $("#id_origin_link").val(data.short_url);
          $("#shortenButton").hide();
          $("#copyButton").show();
        }
      }
    });
  };


  /* Binding */
  $('#copyButton').click(copyLink);

  // Ajax setup.
  // Add CSRF token to header.
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  // AJAX post originUrl
  $("#urlForm").submit(postOriginUrl);

});