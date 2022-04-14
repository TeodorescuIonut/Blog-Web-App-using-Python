const firstPost = document.getElementsByClassName('posts')[0];
if (firstPost != undefined){
    firstPost.classList.add('col-md-12');
}


var file = document.getElementById('formFile');
if (file != null){
    file.onchange = function(e) {
      var ext = this.value.match(/\.([^\.]+)$/i)[1];
      switch (ext.toLowerCase()) {
        case 'jpg':
        case 'bmp':
        case 'png':
        case 'tif':
        case 'jpeg':
          break;
        default:
          alert('Not allowed! Please add a valid type - jpg, bmp, png,tif or jpeg');
          this.value = '';
    };
if(event.target.files.length > 0){
    var src = URL.createObjectURL(event.target.files[0]);
    var preview = document.getElementById("file-ip-1-preview");
    preview.src = src;
    preview.style.display = "block";
  };
 };

}
