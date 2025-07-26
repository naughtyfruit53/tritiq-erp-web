// src/static/js/vouchers.js
function viewVoucher(id) {
    // Fetch and display voucher details
    fetch(`/api/v1/erp/voucher_types/${id}`)
        .then(response => response.json())
        .then(voucher => {
            alert(`Voucher: ${voucher.name}\nModule: ${voucher.module_name}`);
        });
}