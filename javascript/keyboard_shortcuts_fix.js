(() => {
    function event_handler(event) {
        event.stopPropagation();
    }
    
    // Function to disable MkDocs Material keyboard shortcuts
    function disableKeyboardShortcuts() {
        document.addEventListener('keydown', event_handler, true);
        console.log('Keyboard Shortcuts disabled 🖖')
    }
    
    // Function to enable MkDocs Material keyboard shortcuts
    function enableKeyboardShortcuts() {
        document.removeEventListener('keydown', event_handler, true);
        console.log('Keyboard Shortcuts enabled')
    }

    // Create a MutationObserver to watch for changes in the document
    const observer = new MutationObserver(() => {
        const installDialog = document.querySelector('body > ewt-install-dialog');
        
        if (installDialog) {
            // If the install dialog is present, disable keyboard shortcuts
            disableKeyboardShortcuts();
        } else {
            // If the install dialog is not present, enable keyboard shortcuts
            enableKeyboardShortcuts();
        }
    });

    document.addEventListener('DOMContentLoaded', () => {
        // Start observing the document body for child additions/removals
        observer.observe(document.body, { childList: true });
    });
})()