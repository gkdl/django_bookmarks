
/* ssiteUrl, staticUrl = 웹사이트의 기본 URL 및 정적 파일의 기본 URL이다*/
/* minWidth 및 minHeight = 북마클릿이 사이트에서 수집할 이미지의 최소 너비와 높이이다.*/
const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minWidth = 250;
const minHeight = 250;

let head = document.getElementsByTagName('head')[0];  // Get HTML head element
let link = document.createElement('link'); // Create new link Element
link.rel = 'stylesheet'; // set the attributes for link element
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random()*9999999999999999);
head.appendChild(link);  // Append link element to HTML head

/*load HTML*/
let body = document.getElementsByTagName('body')[0];
boxHtml = `
  <div id="bookmarklet">
    <a href="#" id="close">&times;</a>
    <h1>Select an image to bookmark:</h1>
    <div class="images"></div>
  </div>`;
body.innerHTML += boxHtml;

function bookmarkletLaunch() {
    console.log('bookmarklet launched');
  let bookmarklet = document.getElementById('bookmarklet');
  let imagesFound = bookmarklet.querySelector('.images');

  // clear images found
  imagesFound.innerHTML = '';
  // display bookmarklet
  bookmarklet.style.display = 'block';

  // close event
  bookmarklet.querySelector('#close').addEventListener('click', function(){
    bookmarklet.style.display = 'none'
  });

  // find images in the DOM with the minimum dimensions
  let images = document.querySelectorAll('img[src$=".jfif"], img[src$=".jpeg"], img[src$=".png"]');

  images.forEach(image => {
    if(image.naturalWidth >= minWidth
       && image.naturalHeight >= minHeight)
    {
      let imageFound = document.createElement('img');
      imageFound.src = image.src;
      imagesFound.append(imageFound);
    }
  })

  // select image event
  imagesFound.querySelectorAll('img').forEach(image => {
    image.addEventListener('click', function(event){
      let imageSelected = event.target;
      bookmarklet.style.display = 'none';
      window.open(siteUrl + 'images/create/?url='
                  + encodeURIComponent(imageSelected.src)
                  + '&title='
                  + encodeURIComponent(document.title),
                  '_blank');
    })
  })
}

// launch the bookmkarklet
bookmarkletLaunch();
