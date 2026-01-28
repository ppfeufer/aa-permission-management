/* global bootstrap, DataTable, permissionManagamentSettings */

$(document).ready(() => {
    'use strict';

    /**
     * Bootstrap tooltip
     *
     * @param {string} [selector=.aa-permission-management] Selector for the tooltip elements, defaults to 'body'
     *                                                      to apply to all elements with the data-bs-tooltip attribute.
     *                                                      Example: 'body', '.my-tooltip-class', '#my-tooltip-id'
     *                                                      If you want to apply it to a specific element, use that element's selector.
     *                                                      If you want to apply it to all elements with the data-bs-tooltip attribute,
     *                                                      use 'body' or leave it empty.
     * @param {string} [namespace=aa-permission-management] Namespace for the tooltip
     * @returns {void}
     */
    const _bootstrapTooltip = ({selector = '.aa-permission-management', namespace = 'aa-permission-management'}) => {
        document.querySelectorAll(`${selector} [data-bs-tooltip="${namespace}"]`)
            .forEach((tooltipTriggerEl) => {
                // Dispose existing tooltip instance if it exists
                const existing = bootstrap.Tooltip.getInstance(tooltipTriggerEl);
                if (existing) {
                    existing.dispose();
                }

                // Remove any leftover tooltip elements
                $('.bs-tooltip-auto').remove();

                // Create new tooltip instance
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
    };

    /**
     * DataTable initialization complete handler
     *
     * @param selector
     * @private
     */
    const _initComplete = (selector) => {
        _bootstrapTooltip({selector: selector});
    };

    // ColumnControl configuration to remove controls from specific columns
    const removeColumnControl = [
        {
            target: 0,
            content: []
        },
        {
            target: 1,
            content: []
        }
    ];

    /**
     * Create and return a DataTable instance.
     *
     * @param selector
     * @param ajaxUrl
     * @return {DataTable}
     */
    const createDataTable = (selector, ajaxUrl) => {
        const columnDefs = [
            {
                targets: [1, 2],
                sortable: false,
                searchable: false,
                columnControl: removeColumnControl,
            },
            {
                target: 2,
                class: 'text-end',
            }
        ];

        return new DataTable(selector, {
            ...permissionManagamentSettings.dataTable,
            ajax: ajaxUrl,
            columnDefs,
            order: [[0, 'asc']],
            initComplete: () => {
                const tableApi = $(selector).DataTable();

                _initComplete(selector);
                tableApi.on('draw.dt', () => _initComplete(selector));
            },
        });
    };

    // Initialize DataTables
    [
        {selector: '#table-groups', url: permissionManagamentSettings.url.api.getGroups},
        {selector: '#table-states', url: permissionManagamentSettings.url.api.getStates},
    ].forEach(({selector, url}) => createDataTable(selector, url));
});
