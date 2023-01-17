function navigate(newBlock) {
    console.log(newBlock)
    window.location.href = 'mining/completed';  // Redirects user to the /mining/completed route when 'mining' is finished
}

fetch('mine')
    .then(response => {
        // get object returned from Mine() function
        const newBlock = response.json();
        navigate(newBlock);
    });
