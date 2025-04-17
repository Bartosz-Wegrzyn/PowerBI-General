document.addEventListener('DOMContentLoaded', () => {
    // Function to navigate to the CRM entity page
    const navigateToEntity = (event, entityType, inputId) => {
        const entityId = document.getElementById(inputId).value || document.getElementById(inputId).placeholder;
        const environment = document.getElementById('environment').value;
        const url = `https://${environment}.crm4.dynamics.com/main.aspx?appid=5b34d60d-00be-e911-a830-000d3a2aa91d&pagetype=entityrecord&etn=${entityType}&id=${entityId}`;
        
        // Open the URL in a new tab
        window.open(url, "_blank");
    };

    // Attach event listeners to all buttons
    document.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', (event) => {
            const entityType = button.dataset.entityType;
            const inputId = button.dataset.inputId;
            navigateToEntity(event, entityType, inputId);
        });
    });
});
