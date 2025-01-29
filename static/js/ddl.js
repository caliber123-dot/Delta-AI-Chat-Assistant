function toggleDropdown() {
    document.getElementById("dropdownMenu").classList.toggle("show");
}

function selectOnlyOne(checkbox) {
    let checkboxes = document.querySelectorAll('.dropdown-content input[type="checkbox"]');
    checkboxes.forEach(cb => {
        if (cb !== checkbox) cb.checked = false;
    });

    let buttonText = document.getElementById("buttonText");    
    if(checkbox.checked == false)
        checkbox.checked = true;
    // alert(checkbox.checked);
    buttonText.innerText = checkbox.checked ? checkbox.value : checkbox.value;

    document.getElementById("dropdownMenu").classList.remove("show");
}

function submitSelection() {
    let retval;
    let selectedCheckbox = document.querySelector('.dropdown-content input[type="checkbox"]:checked');
    // let label = document.getElementById("selectedLabel");

    if (selectedCheckbox) {
        retval = selectedCheckbox.value;
        // alert(selectedCheckbox.value);
        // label.innerText = "Selected Value: " + selectedCheckbox.value;
    } else {
        retval = "None";
        // alert("None");
    }
    return retval;
}

// Ensure the correct default selection on page load
window.onload = function () {
    let defaultCheckbox = document.querySelector('.dropdown-content input[type="checkbox"]:checked');
    if (defaultCheckbox) {
        document.getElementById("buttonText").innerText = defaultCheckbox.value;
        document.getElementById("selectedLabel").innerText = "Selected Value: " + defaultCheckbox.value;
    }
};

// Close the dropdown if clicked outside
window.onclick = function(event) {
    if (!event.target.matches('.dropdown-button') && !event.target.matches('.arrow')) {
        let dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}