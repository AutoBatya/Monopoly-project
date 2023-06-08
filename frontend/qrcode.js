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