document.addEventListener('DOMContentLoaded', () => {
    // Load data from localStorage immediately when page loads
    const billData = localStorage.getItem('billData');
    
    if (billData) {
        const tableBody = document.getElementById('itemTable').getElementsByTagName('tbody')[0];
        // Clear existing dummy data first
        tableBody.innerHTML = '';
        // Add the stored data
        tableBody.innerHTML = billData;
        
        // Remove delete buttons after loading the data
        const deleteButtons = tableBody.querySelectorAll('.delete-btn, button');
        deleteButtons.forEach(button => {
            button.parentElement.remove(); // Remove the entire Actions cell
        });
        
        console.log('Bill data loaded:', billData);
    }
    
    // Also listen for broadcast channel (backup method)
    const channel = new BroadcastChannel('page-channel');
    
    channel.onmessage = (event) => {
        if(event.data === 'green') {
            const billData = localStorage.getItem('billData');
            if (billData) {
                const tableBody = document.getElementById('itemTable').getElementsByTagName('tbody')[0];
                tableBody.innerHTML = '';
                tableBody.innerHTML = billData;
                
                // Remove delete buttons here too
                const deleteButtons = tableBody.querySelectorAll('.delete-btn, button');
                deleteButtons.forEach(button => {
                    button.parentElement.remove();
                });
                
                console.log('Bill data updated via broadcast:', billData);
            }
        }
    };
});