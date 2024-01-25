document.addEventListener('DOMContentLoaded', function () {
    // JavaScript for handling file drop and triggering the form submission
    function handleFileDrop(event) {
        event.preventDefault();
        event.stopPropagation();

        const fileInput = document.querySelector('input[type="file"]');
        const file = event.dataTransfer.files[0];

        if (file) {
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;

            // Automatically trigger the form submission
            document.querySelector('form').submit();

            // Update the file name text
            document.querySelector('#selected-file-name').textContent = `Selected File: ${file.name}`;
        }
    }

    function preventDefaultBehavior(event) {
        event.preventDefault();
        event.stopPropagation();
    }

    // Event listeners for drag and drop
    const fileDropBox = document.querySelector('.file-drop-box');

    fileDropBox.addEventListener('dragenter', preventDefaultBehavior);
    fileDropBox.addEventListener('dragover', preventDefaultBehavior);
    fileDropBox.addEventListener('dragleave', preventDefaultBehavior);
    fileDropBox.addEventListener('drop', handleFileDrop);

    // Event listener to submit the form when a file is selected
    const fileInput = document.querySelector('input[type="file"]');
    fileInput.addEventListener('change', function () {
        this.form.submit();
        // Update the file name text
        document.querySelector('#selected-file-name').textContent = `Selected File: ${this.files[0].name}`;
    });

    // JavaScript code to draw the bar chart
    const barChartCanvas = document.getElementById('security-issues-bar-chart');
    const barCtx = barChartCanvas.getContext('2d');

    // Read the data attributes and parse the JSON data
    const issueNames = JSON.parse(barChartCanvas.getAttribute('data-issue-names'));
    const issueCounts = JSON.parse(barChartCanvas.getAttribute('data-issue-counts'));

    const barChartData = {
        labels: issueNames,
        datasets: [{
            label: 'Security Issues',
            data: issueCounts,
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)', // Blue
                'rgba(255, 99, 132, 0.2)', // Red
                'rgba(255, 205, 86, 0.2)' // Yellow
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)', // Blue
                'rgba(255, 99, 132, 1)', // Red
                'rgba(255, 205, 86, 1)' // Yellow
            ],
            borderWidth: 1
        }]
    };

    new Chart(barCtx, {
        type: 'bar',
        data: barChartData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
