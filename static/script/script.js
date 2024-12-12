

  function enabletxt(field_id) {
      const field = document.getElementById(field_id).readOnly = false;
  }



  function enabletxtmultiple(...args) {
    args.forEach(arg => enabletxt(arg));
    }



  function disbletxt(field_id) {
    const field = document.getElementById(field_id).readOnly = true;
  }



  function disbletxtmultiple(...args) {
    args.forEach(arg => disbletxt(arg));
    }


  function hide_unhide(field_id){
    
    x=document.getElementById(field_id);

    if (x.hidden) {
      x.hidden = false;
    } else {
      x.hidden = true;
    }

  }