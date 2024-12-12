function enableTxt(field_id) {
    document.getElementById(field_id).readOnly = false;
  }



  function printArgs(...args) {
    args.forEach(arg => console.log(arg));
}