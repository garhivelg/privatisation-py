    $(function() {
      $('#filterClick').bind('click', function() {
        $('#filter').toggle();
      });
    });

    $(function() {
      $('#full_addr').bind('change', function() {
        $.post('/parse/addr', {
          addr: $('input[name="full_addr"]').val()
        }, function(data) {
          $("#addr_type").val(data.addr_type).change();
          $("#addr_name").val(data.addr_name);
          $("#addr_build").val(data.addr_build);
          $("#addr_flat").val(data.addr_flat);
        }, "json");
        return false;
      });
    });

    // Owner
    $(function() {
      $('#full_owner').bind('change', function() {
        $.post('/parse/owner', {
          owner: $('input[name="full_owner"]').val()
        }, function(data) {
          $("#owner").val(data.owner);
          $("#owner_init").val(data.owner_init);
        }, "json");
        return false;
      });
    });

    $(function() {
      $('.owner_names input').bind('change', function() {
        first_name = $('#owner_firstname').val();
        middle_name = $('#owner_middlename').val();
        if (first_name.length > 0) {
          first_name = first_name[0] + ".";
        }
        if (middle_name.length > 0) {
          middle_name = middle_name[0] + ".";
        }
        $("#owner_init").val(first_name + middle_name);
          return false;
        });
      });

    // Autocomplete
    $('.autocomplete').autocomplete({
      serviceUrl: '/list/streetnames.json',
      onSelect: function (suggestion) {
        $("#city_id").val(suggestion.data.city_id).change()
        $("#addr_type").val(suggestion.data.addr_type)
        $("#addr_name").val(suggestion.data.addr_name)
      }
    });

