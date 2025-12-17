/*
    window.bookmarklet이 정의되었으면서 참으로 간주되는 값이면 bookmarkletLaunch 함수가 실행된다.
    bookmarklet.js 스크립트에서 bookmarkletLaunch 를 전역 함수로 정의한다.
 */
(function(){
  if(!window.bookmarklet) {
    bookmarklet_js = document.body.appendChild(document.createElement('script'));
    bookmarklet_js.src = '//127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*9999999999999999);
    window.bookmarklet = true;
  }
  else {
    bookmarkletLaunch();
  }
})();
