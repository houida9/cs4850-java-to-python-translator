// Disable download buttons when the text area is empty
setInterval(function() { 
  if(document.getElementById('javaTextArea').value.trim().length > 0) { 
      document.getElementById('javadownload').disabled = false; 
  } else{
    document.getElementById('javadownload').disabled = true; 
  }

  if(document.getElementById('pythonTextArea').value.trim().length > 0){ 
      document.getElementById('pythondownload').disabled = false;
  } else{
    document.getElementById('pythondownload').disabled = true;
  }
}, 1000);

// Click listener for the Python download button
function downloadPythonFile(filename){
    var element = document.createElement('a');
    let text = document.getElementById('pythonTextArea').value;
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

// Click listener for the Java download button
function downloadJavaFile(filename){
    var element = document.createElement('a');
    let text = document.getElementById('javaTextArea').value;
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

// Copy uploaded file to the Java text area
document.getElementById('inputfile')
  .addEventListener('change', function() {
      var fr = new FileReader();
      fr.onload = function(){

          document.getElementById('javaTextArea')
              .value = fr.result;
      }

      fr.readAsText(this.files[0]);
      document.getElementById('inputfile').value = ''; // change to '' if u want reload behavior
  })

// Activate TAB spaces in Java text area
document.getElementById('javaTextArea').addEventListener('keydown', function(e) {
    if (e.key == 'Tab') {
      e.preventDefault();
      var start = this.selectionStart;
      var end = this.selectionEnd;

      this.value = this.value.substring(0, start) +
        "\t" + this.value.substring(end);

      this.selectionStart =
        this.selectionEnd = start + 1;
    }
});
