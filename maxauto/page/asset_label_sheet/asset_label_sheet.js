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
    const logoCandidates = [
        '/files/company-logo.png',
        frappe.boot?.sysdefaults?.app_logo,
        frappe.boot?.favicon,
        frappe.boot?.app_logo,
        '/assets/frappe/images/frappe-framework-logo.svg'
    ].filter(Boolean);

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
                padding: 1.4mm;
                box-sizing: border-box;
                font-family: Arial, sans-serif;
                font-size: 5.2px;
                display: flex;
                flex-direction: column;
                gap: 0.8mm;
            }

            .header {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 1.2mm;
                font-weight: bold;
                min-height: 5.8mm;
                text-align: center;
            }

            .header img {
                width: auto;
                height: 5.2mm;
                max-width: 14mm;
                object-fit: contain;
            }

            .logo-fallback {
                width: 12mm;
                height: 5.2mm;
                border: 1px solid #999;
                border-radius: 1mm;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 4.8px;
                color: #666;
                flex: 0 0 auto;
            }

            .company-name {
                font-size: 5.8px;
                font-weight: 700;
                line-height: 1.1;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                max-width: 34mm;
            }

            .label-body {
                display: grid;
                grid-template-columns: 1fr 12.5mm;
                column-gap: 1mm;
                align-items: center;
                min-height: 12.8mm;
                flex: 1;
            }

            .label-details {
                display: flex;
                flex-direction: column;
                justify-content: center;
                gap: 0.65mm;
                min-width: 0;
                align-self: stretch;
            }

            .detail-row {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                line-height: 1.15;
            }

            .detail-row.asset-id {
                font-weight: 700;
                font-size: 6.1px;
            }

            .detail-row.location {
                font-size: 5.1px;
                color: #222;
            }

            .detail-row.calibration {
                font-size: 4.8px;
                color: #444;
            }

            .qr {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 12.5mm;
                height: 12.5mm;
                overflow: hidden;
            }

            .label-footer {
                border-top: 0.35mm solid #888;
                padding-top: 0.55mm;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 4.5px;
                color: #444;
                overflow: hidden;
            }

            .contact-text {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                line-height: 1.1;
                font-weight: 600;
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
            }
        </style>
    `);

    const qrScript = document.createElement('script');
    qrScript.src = "https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js";
    document.head.appendChild(qrScript);

    qrScript.onload = () => {
        fetchCompanyLogo();

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

    function fetchCompanyLogo() {
        const defaultCompany = frappe.defaults.get_default('company');
        if (!defaultCompany) return;

        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Company',
                filters: { name: defaultCompany },
                fieldname: ['company_logo']
            },
            callback: function (r) {
                const companyLogo = r?.message?.company_logo;
                if (companyLogo) {
                    logoCandidates.unshift(companyLogo);
                }
            }
        });
    }

    function setLogoWithFallback(imgEl) {
        if (!imgEl) {
            return;
        }

        const fallbackEl = imgEl.parentElement?.querySelector('.logo-fallback');

        if (!logoCandidates.length) {
            imgEl.style.display = 'none';
            if (fallbackEl) fallbackEl.style.display = 'flex';
            return;
        }

        let index = 0;
        const tryNext = () => {
            if (index >= logoCandidates.length) {
                imgEl.style.display = 'none';
                if (fallbackEl) fallbackEl.style.display = 'flex';
                return;
            }

            const src = logoCandidates[index++];
            const probe = new Image();
            probe.onload = () => {
                imgEl.setAttribute('src', src);
                imgEl.style.display = 'block';
                if (fallbackEl) fallbackEl.style.display = 'none';
            };
            probe.onerror = tryNext;
            probe.src = src;
        };

        tryNext();
    }

    function getCompanyInitials() {
        const company = frappe.defaults.get_default('company') || 'Company';
        const parts = company.trim().split(/\s+/).filter(Boolean);
        if (!parts.length) return 'CO';
        return parts.slice(0, 2).map(part => part[0].toUpperCase()).join('');
    }

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
                    <img class="company-logo" alt="" style="display:none;">
                    <div class="logo-fallback">${frappe.utils.escape_html(getCompanyInitials())}</div>
                    <div class="company-name">${frappe.utils.escape_html(frappe.defaults.get_default('company') || 'Company')}</div>
                </div>

                <div class="label-body">
                    <div class="label-details">
                        <div class="detail-row asset-id">${frappe.utils.escape_html(asset.name || '')}</div>
                        <div class="detail-row location">${frappe.utils.escape_html(asset.location || 'No Location')}</div>
                        <div class="detail-row calibration">
                            ${optionalCalibrationField && asset[optionalCalibrationField]
                                ? 'CAL: ' + frappe.datetime.str_to_user(asset[optionalCalibrationField])
                                : ''}
                        </div>
                    </div>
                    <div class="qr"></div>
                </div>

                <div class="label-footer">${frappe.utils.escape_html(asset.name || '')}</div>
                </div>
            `;

            const contactText = 'If found, Please contact : +91 9845903187';
            const footer = label.querySelector('.label-footer');
            footer.innerHTML = `
                <div class="contact-text">${frappe.utils.escape_html(contactText)}</div>
            `;

            grid.appendChild(label);

            const logoImage = label.querySelector('.company-logo');
            setLogoWithFallback(logoImage);

            new QRCode(label.querySelector('.qr'), {
                text: url,
                width: 32,
                height: 32,
                correctLevel: QRCode.CorrectLevel.M
            });
        });
    }

    function printLabelsOnly() {
        const grid = document.getElementById('label-grid');
        if (!grid || !grid.innerHTML.trim()) {
            frappe.msgprint(__('No labels available to print.'));
            return;
        }

        const printWindow = window.open('', '_blank', 'width=1100,height=900');
        if (!printWindow) {
            frappe.msgprint(__('Unable to open print window. Please allow pop-ups for this site.'));
            return;
        }

        const printStyles = `
            <style>
                @page { size: A4; margin: 8mm; }
                body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
                .label-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 60mm);
                    gap: 5mm;
                }
                .label {
                    width: 60mm;
                    height: 25mm;
                    border: 1px solid #000;
                    padding: 1.4mm;
                    box-sizing: border-box;
                    font-size: 5.2px;
                    display: flex;
                    flex-direction: column;
                    gap: 0.8mm;
                }
                .header {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 1.2mm;
                    font-weight: bold;
                    min-height: 5.8mm;
                    text-align: center;
                }
                .header img {
                    width: auto;
                    height: 5.2mm;
                    max-width: 14mm;
                    object-fit: contain;
                }
                .logo-fallback {
                    width: 12mm;
                    height: 5.2mm;
                    border: 1px solid #999;
                    border-radius: 1mm;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 4.8px;
                    color: #666;
                    flex: 0 0 auto;
                }
                .company-name {
                    font-size: 5.8px;
                    font-weight: 700;
                    line-height: 1.1;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    max-width: 34mm;
                }
                .label-body {
                    display: grid;
                    grid-template-columns: 1fr 12.5mm;
                    column-gap: 1mm;
                    align-items: center;
                    min-height: 12.8mm;
                    flex: 1;
                }
                .label-details {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    gap: 0.65mm;
                    min-width: 0;
                    align-self: stretch;
                }
                .detail-row {
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    line-height: 1.15;
                }
                .detail-row.asset-id {
                    font-weight: 700;
                    font-size: 6.1px;
                }
                .detail-row.location {
                    font-size: 5.1px;
                    color: #222;
                }
                .detail-row.calibration {
                    font-size: 4.8px;
                    color: #444;
                }
                .qr {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 12.5mm;
                    height: 12.5mm;
                    overflow: hidden;
                }
                .label-footer {
                    border-top: 0.35mm solid #888;
                    padding-top: 0.55mm;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 4.5px;
                    color: #444;
                    overflow: hidden;
                }
                .contact-text {
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    line-height: 1.1;
                    font-weight: 600;
                }
            </style>
        `;

        printWindow.document.open();
        printWindow.document.write(`
            <html>
                <head>
                    <title>Asset Label Sheet</title>
                    ${printStyles}
                </head>
                <body>
                    ${grid.outerHTML}
                </body>
            </html>
        `);
        printWindow.document.close();

        printWindow.onload = () => {
            setTimeout(() => {
                printWindow.focus();
                printWindow.print();
                printWindow.onafterprint = () => printWindow.close();
            }, 350);
        };
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
        setTimeout(() => printLabelsOnly(), 250);
    });
};
