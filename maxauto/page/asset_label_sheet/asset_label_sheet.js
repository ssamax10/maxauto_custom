frappe.pages['asset-label-sheet'].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Asset Label Sheet',
        single_column: true
    });

    // Add HTML content directly
    $(wrapper).find('.layout-main-section').html(`
        <div class="toolbar">
            <button class="btn btn-sm btn-primary" id="print-selected">
                Print Selected
            </button>
            <button class="btn btn-sm btn-default" id="select-visible" style="margin-left: 8px;">
                Select Visible
            </button>
            <button class="btn btn-sm btn-default" id="clear-selection" style="margin-left: 4px;">
                Clear
            </button>
            <input
                type="text"
                id="asset-filter"
                placeholder="Search by Asset ID or Location"
                style="margin-left: 12px; min-width: 280px;"
            />
            <span id="asset-count" style="margin-left: 10px; color: #666;"></span>
        </div>

        <div id="asset-list"></div>

        <hr>

        <div class="label-grid" id="label-grid"></div>
    `);

    let allAssets = [];
    let filteredAssets = [];
    const selectedAssets = new Set();
    const baseFields = ['name', 'location'];
    let optionalCalibrationField = null;

    $('head').append(`
        <style>
            @page { size: A4; margin: 8mm; }

            .label-grid {
                display: grid;
                grid-template-columns: repeat(3, 60mm);
                gap: 5mm;
            }

            .label {
                width: 60mm;
                height: 25mm;
                border: 1px solid #000;
                padding: 2mm;
                box-sizing: border-box;
                font-family: Arial, sans-serif;
                font-size: 6px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }

            .header {
                display: flex;
                align-items: center;
                gap: 2mm;
                font-weight: bold;
            }

            .header img { max-height: 6mm; }

            .qr { display: flex; justify-content: center; }

            .asset-tag {
                font-weight: bold;
                font-size: 7px;
                text-align: center;
            }

            .footer {
                display: flex;
                justify-content: space-between;
                font-size: 5.5px;
            }

            #asset-list {
                max-height: 340px;
                overflow: auto;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 6px;
                margin-top: 10px;
            }

            @media print {
                .toolbar, #asset-list { display: none; }

                body.printing-asset-labels .navbar,
                body.printing-asset-labels .layout-side-section,
                body.printing-asset-labels .sidebar,
                body.printing-asset-labels .page-head {
                    display: none !important;
                }

                body.printing-asset-labels .layout-main,
                body.printing-asset-labels .layout-main-section,
                body.printing-asset-labels .main-section {
                    width: 100% !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }
            }
        </style>
    `);

    const qrScript = document.createElement('script');
    qrScript.src = "https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js";
    document.head.appendChild(qrScript);

    qrScript.onload = () => {
        frappe.model.with_doctype('Asset', () => {
            const meta = frappe.get_meta('Asset');
            const availableFields = new Set((meta.fields || []).map(df => df.fieldname));

            if (availableFields.has('custom_calibration_due_date')) {
                optionalCalibrationField = 'custom_calibration_due_date';
            }

            const queryFields = [...baseFields];
            if (optionalCalibrationField) {
                queryFields.push(optionalCalibrationField);
            }

            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Asset',
                    fields: queryFields,
                    limit_page_length: 1000
                },
                callback: function (r) {
                    if (!r.message) return;
                    allAssets = r.message;
                    applyFilter('');
                }
            });
        });
    };

    function renderAssetList(assets) {
        const list = document.getElementById('asset-list');
        list.innerHTML = '';

        document.getElementById('asset-count').textContent = `${assets.length} of ${allAssets.length} assets`;

        if (!assets.length) {
            list.innerHTML = '<div style="color:#777;">No assets match your search.</div>';
            return;
        }

        assets.forEach(a => {
            list.insertAdjacentHTML('beforeend', `
                <label>
                  <input type="checkbox" value="${a.name}" ${selectedAssets.has(a.name) ? 'checked' : ''}>
                  ${a.name} (${a.location || '-'})
                </label><br>
            `);
        });
    }

    function applyFilter(rawText) {
        const text = (rawText || '').trim().toLowerCase();
        filteredAssets = allAssets.filter(asset => {
            const haystack = `${asset.name} ${asset.location || ''}`.toLowerCase();
            return haystack.includes(text);
        });
        renderAssetList(filteredAssets);
    }

    function renderLabels(assets) {
        const grid = document.getElementById('label-grid');
        grid.innerHTML = '';

        assets.forEach(asset => {
            const url = `${location.origin}/app/asset/${asset.name}`;

            const label = document.createElement('div');
            label.className = 'label';

            label.innerHTML = `
                <div class="header">
                  <img src="/files/company-logo.png">
                  <div>${frappe.defaults.get_default('company')}</div>
                </div>

                <div class="qr"></div>

                <div class="asset-tag">${asset.name}</div>

                <div class="footer">
                  <span>${asset.location || ''}</span>
                  <span>
                                        ${optionalCalibrationField && asset[optionalCalibrationField]
                                            ? 'CAL: ' + frappe.datetime.str_to_user(asset[optionalCalibrationField])
                      : ''}
                  </span>
                </div>
            `;

            grid.appendChild(label);

            new QRCode(label.querySelector('.qr'), {
                text: url,
                width: 70,
                height: 70,
                correctLevel: QRCode.CorrectLevel.M
            });
        });
    }

    // Use event delegation since the button is added dynamically
    $(wrapper).on('input', '#asset-filter', function () {
        applyFilter(this.value);
    });

    $(wrapper).on('change', '#asset-list input[type="checkbox"]', function () {
        if (this.checked) {
            selectedAssets.add(this.value);
        } else {
            selectedAssets.delete(this.value);
        }
    });

    $(wrapper).on('click', '#select-visible', function () {
        filteredAssets.forEach(asset => selectedAssets.add(asset.name));
        renderAssetList(filteredAssets);
    });

    $(wrapper).on('click', '#clear-selection', function () {
        selectedAssets.clear();
        renderAssetList(filteredAssets);
    });

    $(wrapper).on('click', '#print-selected', function() {
        const checked = [...selectedAssets];

        if (!checked.length) {
            frappe.msgprint(__('Please select at least one asset to print labels.'));
            return;
        }

        const selected = allAssets.filter(a => checked.includes(a.name));
        if (!selected.length) {
            frappe.msgprint(__('No matching assets found for selected rows.'));
            return;
        }

        renderLabels(selected);

        document.body.classList.add('printing-asset-labels');
        setTimeout(() => {
            window.print();
            setTimeout(() => document.body.classList.remove('printing-asset-labels'), 500);
        }, 300);
    });
};
