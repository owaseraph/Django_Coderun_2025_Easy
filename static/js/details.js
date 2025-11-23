document.getElementById('summaryBtn').addEventListener('click', function() {
        const summaryDetails = document.getElementById('summaryDetails');
        if (summaryDetails.style.display === 'none') {
            summaryDetails.style.display = 'block';
            this.textContent = 'Hide Summary';
        } else {
            summaryDetails.style.display = 'none';
            this.textContent = 'Show Summary';
        }
    });