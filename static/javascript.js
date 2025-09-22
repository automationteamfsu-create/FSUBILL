// Wait for the DOM to load
let tableBody;
document.addEventListener('DOMContentLoaded', function() {
    

    // localStorage.clear();
    const form = document.getElementById('itemForm');
    tableBody = document.getElementById('itemTable').getElementsByTagName('tbody')[0];
    const totalCostElement = document.getElementById('totalCost');
    
    let itemCounter = 0;

    // Function to calculate and update total cost
    function updateTotalCost() {
        const rows = tableBody.getElementsByTagName('tr');
        let total = 0;
        
        for (let i = 0; i < rows.length; i++) {
            const amountCell = rows[i].getElementsByTagName('td')[3]; // Changed from index 2 to 3
            if (amountCell) {
                total += parseFloat(amountCell.innerText) || 0;
            }
        }
        
        totalCostElement.innerText = total.toFixed(2);
    }

    // Function to delete a row
    function deleteRow(button) {
        const row = button.closest('tr');
        row.remove();
        updateTotalCost();
    }

    // Make deleteRow function globally available
    window.deleteRow = deleteRow;

    // Handle form submission
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Get form values
        const date = document.getElementById('date').value;
        const category = document.getElementById('category').value;
        const description = document.getElementById('description').value; // Added description
        const amount = parseFloat(document.getElementById('amount').value);

        // Validate inputs
        if (!date || !category || !description || isNaN(amount)) { // Added description validation
            alert('Please fill in all fields correctly.');
            return;
        }

        // Create a new row
        const newRow = tableBody.insertRow();
        itemCounter++;

        // Add cells with data
        newRow.insertCell(0).innerText = date;
        newRow.insertCell(1).innerText = category;
        newRow.insertCell(2).innerText = description; // Added description cell
        newRow.insertCell(3).innerText = amount.toFixed(2); // Amount moved to index 3
        
        // Add delete button
        const actionsCell = newRow.insertCell(4); // Actions moved to index 4
        actionsCell.innerHTML = '<button onclick="deleteRow(this)" class="delete-btn">Delete</button>';

        // Update total cost
        updateTotalCost();

        // Clear the form
        // form.reset();
        
        // Show success message
        showMessage('Item added successfully!', 'success');
    });

    // Function to show messages
    function showMessage(message, type) {
        // Remove existing message if any
        const existingMessage = document.querySelector('.message');
        if (existingMessage) {
            existingMessage.remove();
        }

        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.innerText = message;
        
        // Insert message after the form
        form.parentNode.insertBefore(messageDiv, form.nextSibling);
        
        // Remove message after 3 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }

}
);
function generateBill() {
    // Check if there's any data to transfer
    if (tableBody.children.length === 0) {
        alert("No items to generate bill. Please add some items first.");
        return;
    }
    
    // Get bill information
    const billTitle = document.getElementById('billTitle').value;
    const billDate = document.getElementById('billDate').value;
    
    // Validate bill information
    if (!billTitle || !billDate) {
        alert("Please fill in both Bill Title and Bill Date before generating the bill.");
        return;
    }
    
    // Collect table data
    const rows = tableBody.querySelectorAll("tr");
    const tableData = [];

    rows.forEach(row => {
        const cells = row.querySelectorAll("td");
        const rowData = [];

        cells.forEach(cell => {
            rowData.push(cell.innerText.trim()); // Get text only
        });

        tableData.push(rowData);
    });

    // Create data object
    const data = {
        title: billTitle,
        date: billDate,
        table: tableData  // array of arrays
    };

    console.log("Data to send:", data);

    // Create a form dynamically
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/generate-bill';
    form.enctype = 'multipart/form-data'; // Important for file uploads

    // Add all fields as hidden inputs
    for (const key in data) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;

        if (typeof data[key] === "object") {
            input.value = JSON.stringify(data[key]);
        } else {
            input.value = data[key];
        }

        // Optional debug attribute
        input.setAttribute('data-debug', input.value);
        form.appendChild(input);
    }

    // Add all file inputs
    const fileInputs = document.querySelectorAll('input[type="file"][name="supportingImages"]');
    fileInputs.forEach((fileInput, index) => {
        if (fileInput.files.length > 0) {
            const clonedInput = fileInput.cloneNode();
            clonedInput.name = `supportingImage_${index}`; // Unique name per file
            form.appendChild(clonedInput);

            // Transfer the file to the cloned input
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(fileInput.files[0]);
            clonedInput.files = dataTransfer.files;
        }
    });

    // Append the form to the document and submit
    document.body.appendChild(form);
    form.submit();
}
