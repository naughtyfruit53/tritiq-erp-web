// src/static/js/vendors.js
let editVendorId = null;

function addVendor() {
    document.getElementById('formTitle').innerText = 'Add Vendor';
    document.getElementById('vendorForm').style.display = 'block';
    document.getElementById('vendorFormElement').reset();
    editVendorId = null;
}

function editVendor(id) {
    editVendorId = id;
    document.getElementById('formTitle').innerText = 'Edit Vendor';
    // Fetch vendor data via API and populate form
    fetch(`/api/v1/erp/vendors/${id}`)
        .then(response => response.json())
        .then(vendor => {
            document.getElementById('name').value = vendor.name;
            document.getElementById('contact_no').value = vendor.contact_no;
            document.getElementById('address1').value = vendor.address1;
            document.getElementById('address2').value = vendor.address2 || '';
            document.getElementById('city').value = vendor.city;
            document.getElementById('state').value = vendor.state;
            updateStateCode();
            document.getElementById('pin').value = vendor.pin;
            document.getElementById('gst_no').value = vendor.gst_no || '';
            document.getElementById('pan_no').value = vendor.pan_no || '';
            document.getElementById('email').value = vendor.email || '';
            document.getElementById('vendorForm').style.display = 'block';
        });
}

function saveVendor() {
    const form = document.getElementById('vendorFormElement');
    if (!form.checkValidity()) {
        alert('All mandatory fields are required');
        return;
    }
    const data = {
        name: document.getElementById('name').value,
        contact_no: document.getElementById('contact_no').value,
        address1: document.getElementById('address1').value,
        address2: document.getElementById('address2').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        state_code: document.getElementById('state_code').value,
        pin: document.getElementById('pin').value,
        gst_no: document.getElementById('gst_no').value,
        pan_no: document.getElementById('pan_no').value,
        email: document.getElementById('email').value
    };
    const method = editVendorId ? 'PUT' : 'POST';
    const url = editVendorId ? `/vendors/edit/${editVendorId}` : '/vendors';
    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            location.reload();
        } else {
            alert('Failed to save vendor');
        }
    });
}

function deleteVendor(id) {
    if (confirm('Confirm delete?')) {
        fetch(`/vendors/delete/${id}`, {method: 'POST'})
            .then(() => location.reload());
    }
}

function importExcel() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.xlsx, .xls';
    input.onchange = (e) => {
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('file', file);
        fetch('/vendors/import', {
            method: 'POST',
            body: formData
        }).then(() => location.reload());
    };
    input.click();
}

function exportExcel() {
    window.location.href = '/vendors/export';
}

function downloadSample() {
    window.location.href = '/vendors/sample';
}

function updateStateCode() {
    const state = document.getElementById('state').value;
    const states = {{ states|tojson }};
    const codes = {{ states_dict|tojson }};  // Assume states_dict passed to template
    document.getElementById('state_code').value = codes[state] || '';
}

function cancelForm() {
    document.getElementById('vendorForm').style.display = 'none';
}

document.getElementById('state').addEventListener('change', updateStateCode);