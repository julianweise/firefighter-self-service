/* globals feather:false */

(function () {
    'use strict'
    feather.replace()
}())

$('#confirmModal').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget);
    const title = button.data('title');
    const body = button.data('body');
    const post = button.data('post');
    const modal = $(this);
    modal.find('.modal-title').text(title);
    modal.find('.modal-body-text').text(body);
    console.log(post);
    modal.find('.modal-footer form').attr('action', post);
})

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})