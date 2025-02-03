// include.js

// Function to insert the logo image and the styles
(function() {
  // Create the image element and set its attributes
  const logoImg = document.createElement('img');
  logoImg.src = './assets/logo.gif';
  logoImg.style.minWidth = '100px';
  logoImg.style.width = '5vw';
  logoImg.style.border = 'none';
  logoImg.style.boxShadow = 'none';
  logoImg.style.position = 'fixed';
  logoImg.style.top = '0';
  logoImg.style.right = '10px';
  logoImg.style.zIndex = '1000';
  logoImg.alt = 'Teapot AI Logo';

  // Insert the image into the body of the page
  document.body.appendChild(logoImg);

  // Create the style element
  const style = document.createElement('style');
  style.textContent = `
    #forkme_banner {
      display: none;
    }

    footer.inner .copyright,
    footer.inner p {
      display: none; /* Hides the original content */
    }

    footer.inner::before {
      content: "418 I'm a teapot (HTCPCP/1.0) | Brewed with 🤍 in NYC | Copyright 2025";
      color: rgb(242, 242, 242);
      display: block;
      text-align: center; /* Center the text */
      font-size: 1.2em; /* Adjust font size if needed */
      font-weight: bold; /* Optional: make the text bold */
      margin-top: 20px; /* Add margin to separate from other elements */
    }
  `;

  // Append the style to the head of the document
  document.head.appendChild(style);
})();
