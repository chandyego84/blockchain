function navigate(newBlock) {
    console.log(newBlock)
    window.location.href = 'mining/completed';  // Redirects user to the /mining/completed route when 'mining' is finished
}

// Makes request to 'mine' endpoint.
// TODO: Ensure base URL is set correctly when deploying site.
fetch('mine')
    .then(response => response.json())
    .then(newBlock => {
        // get object returned from Mine() function
        navigate(newBlock);
    });
