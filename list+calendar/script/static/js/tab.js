alert ("hello world !")

$('[data-open-details]').hover(function (e) {
  e.preventDefault();
  $(this).next().toggleClass('is-active');
  $(this).toggleClass('is-active');
});
