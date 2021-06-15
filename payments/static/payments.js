// Get Stripe publishable key
var baseurl = window.location.origin;
var stripe = {};
fetch(baseurl + "/payments/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  stripe = Stripe(data.publicKey);

  // Event handler
  document.querySelectorAll("#submitPaymentBtn").forEach(item => { 
          item.addEventListener("click", onClickEvent);
      })
  });

  const nav = document.querySelector('.mainNavbar');
  const header = document.querySelector('.js-nav');
  const navHeight = nav.getBoundingClientRect().height;

  const stickyNav = function (entries){
    const [entry] = entries;
    if (!entry.isIntersecting) {
      nav.classList.add('sticky');
    } 
    else{
      nav.classList.remove('sticky');
    } 
  };

  const headerObserver = new IntersectionObserver(
    stickyNav,{
      root:null,
      threshold: 0, // percentage we want visible in the view port with the current target 
      rootMargin: '50px'
    }
  );
  headerObserver.observe(header); 


  function onClickEvent(e){
    try{
        // Get Checkout Session ID
        // Get jobId value 
       var jobId = e.target.value;
      
        fetch(baseurl+"/payments/create-checkout-session/" + jobId)
        .then((result) => { return result.json(); })
        .then((data) => {      
          // Redirect to Stripe Checkout
          return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .then((res) => {
          console.log(res);
        });
    }catch(error){
      console.log(error);
    }
  }