const qrcode = QRCreator(href='#',
{ mode: -1,
  eccl: 0,
  version: 3,
  mask: -1,
  image: 'html',
  modsize: 8,
  margin: 1
});
const content = (qrcode) =>{
  return qrcode.error ?
    `недопустимые исходные данные ${qrcode.error}`:
     qrcode.result;
};

document.getElementById('qrcode').append(content(qrcode));
const url = new URL(window.location.href);
let id = url.searchParams.get("id");
 if (history.pushState) {
        var baseUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
        var newUrl = baseUrl + '?id='+ id;
        history.pushState(null, null, newUrl);
    }
    else {
        console.warn('History API не поддерживается');
    }  
document.getElementById('id').innerHTML = id;
