const firstPost = document.getElementsByClassName("posts")[0];
firstPost.classList.add('col-md-12');

var file = document.getElementById('formFile');

file.onchange = function(e) {
  var ext = this.value.match(/\.([^\.]+)$/)[1];
  switch (ext) {
    case 'jpg':
    case 'bmp':
    case 'png':
    case 'tif':
    case 'jpeg':
      alert('Allowed');
      break;
    default:
      alert('Not allowed');
      this.value = '';
  }
};