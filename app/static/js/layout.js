// Function to show the message container
function showMessage(message, category) {
    var messageContainer = document.getElementById('messageContainer');
    var messageText = document.getElementById('messageText');
    var progressBar = document.getElementById('progressBar');

    // Set the message text
    messageText.innerHTML = message;

    // Set the color based on the category
    switch (category) {
        case 'success':
            messageContainer.style.color = '#00FF00'; // Green
            break;
        case 'danger':
            messageContainer.style.color = '#FF0000'; // Red
            break;
        case 'info':
            messageContainer.style.color = '#FFA500'; // Orange
            break;
        default:
            messageContainer.style.color = '#FFFFFF'; // Default white
    }

    // Show the message container
    messageContainer.classList.add('show');

    // Start the progress bar animation (countdown from left to right)
    progressBar.style.width = '100%';
    progressBar.style.transition = 'width 5s linear';
    setTimeout(function () {
        progressBar.style.width = '0%';
    }, 100);

    // Hide the message container after 5 seconds
    setTimeout(function () {
        messageContainer.classList.remove('show');
    }, 5000); 
}


// Toggle collapse class on button click
document.querySelector('.navbar-toggler').addEventListener('click', function() {
    var sidebar = document.getElementById('sidebar');
    var content = document.getElementById('content');
    sidebar.classList.toggle('collapsed');
    content.classList.toggle('collapsed');
});