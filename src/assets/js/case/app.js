$('#confirm-del').on('show.bs.modal', function(e) {
  $(this).find('.modal-body').html($(e.relatedTarget).data('text'));
  $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
});

