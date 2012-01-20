(
function () {

var root = location.pathname;

var getMyTime = function () {
  return ('' + (new Date()).valueOf()).slice(-6);
};

var onpopstate = function (ev) {
  console.log('on pop state');
  console.log(ev);
};

var pushstate = function (ev) {
  console.log('push state');
  var id = getMyTime();
  history.pushState(id, id, root + id);
};

var replacestate = function (ev) {
  console.log('replace state');
  var id = getMyTime();
  history.replaceState(id, id, root + id);
};

var init = function () {
  $('#pushState').click(pushstate);
  $('#replaceState').click(replacestate);
  $(window).bind('popstate', onpopstate);
};

$(init);

})();