(function() {

$(document).ready(function () {

  // input toggle
  var add = $('button#add')
  var form = $('form#story-form')
  add.show()
  form.hide()
  add.click(function (e) {
    add.hide()
    form.show()
  })

  // display delete links on hover
  $('form.delete').hide()
  $('li').hover(function (e) { $(e.currentTarget).find('form').toggle() })

})

})();
