function navigate() {
    window.location.href = 'mining/completed';  // Redirects user to the /mining/completed route when 'mining' is finished
}

fetch('mine').then(navigate); // Performing 'mining' and then calls navigate() function, declared above