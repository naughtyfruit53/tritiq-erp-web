 // src/static/js/scripts.js
function loadForm(url) {
  fetch(url)
    .then(response => response.json())
    .then(data => {
      // Fill form fields with data
      document.getElementById('po_id').value = data.id;
      document.getElementById('po_number').value = data.po_number;
      document.getElementById('vendor_id').value = data.vendor_id;
      document.getElementById('po_date').value = data.po_date;
      document.getElementById('delivery_date').value = data.delivery_date || '';
      document.getElementById('payment_terms').value = data.payment_terms || '';
      // Clear and populate items table
      const tableBody = document.getElementById('items_table').getElementsByTagBody()[0];
      tableBody.innerHTML = '';
      data.items.forEach(item => addItemRow(item));
      calculateTotal();
    });
}

function clearForm() {
  document.getElementById('purchase_order_form').reset();
  document.getElementById('po_id').value = '';
  document.getElementById('items_table').getElementsByTagBody()[0].innerHTML = '';
  calculateTotal();
}

function addItemRow(item = {}) {
  const tableBody = document.getElementById('items_table').getElementsByTagBody()[0];
  const row = tableBody.insertRow();
  row.innerHTML = `
    <td><select class="form-control product-select" onchange="fetchProductDetails(this)">
      <option value="">Select Product</option>
      <!-- Options loaded via fetch on load -->
    </select><button type="button" class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#addProductModal">Add New</button></td>
    <td><input type="number" class="form-control" name="quantity" value="${item.quantity || ''}" oninput="calculateAmount(this.closest('tr'))"></td>
    <td><input type="number" class="form-control" name="unit_price" value="${item.unit_price || ''}" oninput="calculateAmount(this.closest('tr'))"></td>
    <td><input type="number" class="form-control" name="gst_rate" value="${item.gst_rate || ''}" oninput="calculateAmount(this.closest('tr'))"></td>
    <td><input type="text" class="form-control" name="amount" readonly></td>
    <td><button type="button" class="btn btn-danger" onclick="removeRow(this)">Remove</button></td>
  `;
  // Load product options
  fetch('/api/v1/erp/products/list')
    .then(response => response.json())
    .then(products => {
      const select = row.querySelector('.product-select');
      products.forEach(p => {
        const option = document.createElement('option');
        option.value = p.id;
        option.textContent = p.name;
        select.appendChild(option);
      });
      if (item.product_id) select.value = item.product_id;
    });
}

function removeRow(btn) {
  btn.closest('tr').remove();
  calculateTotal();
}

function calculateAmount(row) {
  const quantity = parseFloat(row.querySelector('[name="quantity"]').value) || 0;
  const unit_price = parseFloat(row.querySelector('[name="unit_price"]').value) || 0;
  const gst_rate = parseFloat(row.querySelector('[name="gst_rate"]').value) || 0;
  const amount = quantity * unit_price * (1 + gst_rate / 100);
  row.querySelector('[name="amount"]').value = amount.toFixed(2);
  calculateTotal();
}

function calculateTotal() {
  const rows = document.getElementById('items_table').getElementsByTagBody()[0].rows;
  let total = 0;
  for (let row of rows) {
    total += parseFloat(row.querySelector('[name="amount"]').value) || 0;
  }
  document.getElementById('total_amount').value = total.toFixed(2);
}

function fetchProductDetails(select) {
  const product_id = select.value;
  if (product_id) {
    fetch(`/api/v1/erp/products/${product_id}`)
      .then(response => response.json())
      .then(data => {
        const row = select.closest('tr');
        row.querySelector('[name="unit_price"]').value = data.unit_price;
        row.querySelector('[name="gst_rate"]').value = data.gst_rate;
        calculateAmount(row);
      });
  }
}

document.getElementById('purchase_order_form').addEventListener('submit', function(e) {
  const items = [];
  const rows = document.getElementById('items_table').getElementsByTagBody()[0].rows;
  for (let row of rows) {
    const item = {
      product_id: row.querySelector('.product-select').value,
      quantity: parseFloat(row.querySelector('[name="quantity"]').value) || 0,
      unit_price: parseFloat(row.querySelector('[name="unit_price"]').value) || 0,
      gst_rate: parseFloat(row.querySelector('[name="gst_rate"]').value) || 0,
      amount: parseFloat(row.querySelector('[name="amount"]').value) || 0
    };
    items.push(item);
  }
  document.getElementById('items_json').value = JSON.stringify(items);
  if (document.getElementById('po_id').value) {
    this.action = `/purchase_orders/${document.getElementById('po_id').value}`;
  }
});

// Modal submit handlers (example for vendor)
document.getElementById('add_vendor_form').addEventListener('submit', function(e) {
  e.preventDefault();
  fetch(this.action, {
    method: 'POST',
    body: new FormData(this)
  }).then(response => {
    if (response.ok) {
      document.getElementById('addVendorModal').querySelector('.btn-close').click();
      // Refresh vendor select
      fetch('/api/v1/erp/vendors/list')
        .then(response => response.json())
        .then(vendors => {
          const select = document.getElementById('vendor_id');
          select.innerHTML = '';
          vendors.forEach(v => {
            const option = document.createElement('option');
            option.value = v.id;
            option.textContent = v.name;
            select.appendChild(option);
          });
        });
    }
  });
});

// Similar for product modal

// For GRN-specific JS in grn.html
function populateFromPO(po_id) {
  if (po_id) {
    fetch(`/api/v1/erp/purchase_orders/${po_id}`)
      .then(response => response.json())
      .then(data => {
        // Populate vendor if needed
        // Clear and populate items table
        const tableBody = document.getElementById('items_table').getElementsByTagBody()[0];
        tableBody.innerHTML = '';
        data.items.forEach(item => {
          const row = tableBody.insertRow();
          row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.hsn_code}</td>
            <td>${item.quantity}</td>
            <td><input type="number" class="form-control" name="received_qty" oninput="validateRow(this.closest('tr'))"></td>
            <td><input type="number" class="form-control" name="accepted_qty" oninput="validateRow(this.closest('tr'))"></td>
            <td><input type="number" class="form-control" name="rejected_qty" oninput="validateRow(this.closest('tr'))"></td>
            <td><input type="text" class="form-control" name="remarks"></td>
          `;
        });
      });
  }
}

function validateRow(row) {
  const received = parseFloat(row.querySelector('[name="received_qty"]').value) || 0;
  const accepted = parseFloat(row.querySelector('[name="accepted_qty"]').value) || 0;
  const rejected = parseFloat(row.querySelector('[name="rejected_qty"]').value) || 0;
  if (accepted + rejected != received) {
    row.querySelector('[name="accepted_qty"]').classList.add('is-invalid');
  } else {
    row.querySelector('[name="accepted_qty"]').classList.remove('is-invalid');
  }
}

function validateGRN() {
  const rows = document.getElementById('items_table').getElementsByTagBody()[0].rows;
  for (let row of rows) {
    validateRow(row);
    if (row.querySelector('.is-invalid')) {
      alert('Accepted + Rejected must equal Received for all items');
      return false;
    }
  }
  const items = [];
  for (let row of rows) {
    const item = {
      name: row.cells[0].textContent,
      hsn_code: row.cells[1].textContent,
      ordered_qty: parseFloat(row.cells[2].textContent) || 0,
      received_qty: parseFloat(row.querySelector('[name="received_qty"]').value) || 0,
      accepted_qty: parseFloat(row.querySelector('[name="accepted_qty"]').value) || 0,
      rejected_qty: parseFloat(row.querySelector('[name="rejected_qty"]').value) || 0,
      remarks: row.querySelector('[name="remarks"]').value
    };
    items.push(item);
  }
  document.getElementById('items_json').value = JSON.stringify(items);
  if (document.getElementById('grn_id').value) {
    document.getElementById('grn_form').action = `/grn/${document.getElementById('grn_id').value}`;
  }
  return true;
}

// Load product options on page load for all voucher forms (generalize as needed)
window.addEventListener('load', function() {
  if (document.getElementById('items_table')) {
    addItemRow();  // Add initial empty row
  }
});