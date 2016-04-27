$('.dot:nth-child(1)').click(function(){
  $('.inside').animate({
    'width' : '7%'
  }, 500);
});
$('.dot:nth-child(2)').click(function(){
  $('.inside').animate({
    'width' : '14%'
  }, 500);
});
$('.dot:nth-child(3)').click(function(){
  $('.inside').animate({
    'width' : '21%'
  }, 500);
});
$('.dot:nth-child(4)').click(function(){
  $('.inside').animate({
    'width' : '28%'
  }, 500);
});
$('.dot:nth-child(5)').click(function(){
  $('.inside').animate({
    'width' : '35%'
  }, 500);
});
$('.dot:nth-child(6)').click(function(){
  $('.inside').animate({
    'width' : '42%'
  }, 500);
});
$('.dot:nth-child(7)').click(function(){
  $('.inside').animate({
    'width' : '49%'
  }, 500);
});
$('.dot:nth-child(8)').click(function(){
  $('.inside').animate({
    'width' : '56%'
  }, 500);
});
$('.dot:nth-child(9)').click(function(){
  $('.inside').animate({
    'width' : '63%'
  }, 500);
});
$('.dot:nth-child(10)').click(function(){
  $('.inside').animate({
    'width' : '70%'
  }, 500);
});
$('.dot:nth-child(11)').click(function(){
  $('.inside').animate({
    'width' : '77%'
  }, 500);
});
$('.dot:nth-child(12)').click(function(){
  $('.inside').animate({
    'width' : '84%'
  }, 500);
});
$('.dot:nth-child(13)').click(function(){
  $('.inside').animate({
    'width' : '91%'
  }, 500);
});$('.dot:nth-child(14)').click(function(){
  $('.inside').animate({
    'width' : '100%'
  }, 500);
});

// modal
$('.modal').wrap('<div class="mask"></div>')
$('.mask').click(function(){
  $(this).fadeOut(300);
  $('.mask article').animate({
    'top' : '-100%'
  }, 300)
});

$('.dot').click(function(){
  var modal = $(this).attr('id');
  $('.mask').has('article.' + modal).fadeIn(300);
  $('.mask article.' + modal).animate({
    'top' : '10%'
  }, 300)
});