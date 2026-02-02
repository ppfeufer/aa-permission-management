/* global bootstrap, DataTable, fetchGet, permissionManagamentSettings */

$(document).ready(() => {
    'use strict';

    /**
     * Bootstrap tooltip
     *
     * @param {string} [selector=.aa-permission-management] Selector for the tooltip elements, defaults to '.aa-permission-management'.
     *                                                      to apply to all elements with the data-bs-tooltip attribute.
     *                                                      Example: 'body', '.my-tooltip-class', '#my-tooltip-id'
     *                                                      If you want to apply it to a specific element, use that element's selector.
     *                                                      If you want to apply it to all elements with the data-bs-tooltip attribute,
     *                                                      use 'body' or leave it empty.
     * @param {string} [namespace=aa-permission-management] Namespace for the tooltip, defined in the data-bs-tooltip attribute, defaults to 'aa-permission-management'.
     * @returns {void}
     * @private
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
     * Show permissions in the permissions container
     *
     * @param {string} permissionType The type of permission to fetch (e.g., 'group', 'state')
     * @param {int} elementId The ID of the element to fetch permissions for
     * @private
     */
    const _showPermissions = (permissionType, elementId) => {
        const elementLoadingSpinner = $('#loading-spinner');
        const elementPermissionsContainer = $('#permissions');

        elementPermissionsContainer.empty().addClass('d-none');
        elementLoadingSpinner.removeClass('d-none');

        const url = permissionManagamentSettings.url.api.getPermissions
            .replace('__permission_type__', permissionType)
            .replace(0, elementId);

        fetchGet({url: url, responseIsJson: false})
            .then((response) => response)
            .then((data) => {
                console.log('Edit Permissions Data:', data);
                elementLoadingSpinner.addClass('d-none');
                elementPermissionsContainer.html(data).removeClass('d-none');
            })
            .catch((error) => {
                console.error('There was a problem with the fetch operation:', error);
            });
    };

    /**
     * DataTable initialization complete handler
     *
     * @param {string} selector Selector for the table element
     * @private
     */
    const _initComplete = (selector) => {
        // Initialize Bootstrap tooltips
        _bootstrapTooltip({selector: selector});

        // Show/Edit permissions button click handler
        $('.btn-edit-permissions').off('click').on('click', (event) => {
            const button = event.currentTarget;
            const permissionType = button.getAttribute('data-permission-type');
            const elementId = button.getAttribute('data-element-id');

            _showPermissions(permissionType, elementId);
        });
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
     * @param {String} selector Selector for the table element
     * @param {String} ajaxUrl URL for AJAX data source
     * @param {Function} [initComplete=() => {}] Callback function to be executed when DataTable initialization is complete
     * @return {DataTable} DataTable instance
     * @private
     */
    const _createDataTable = ({selector, ajaxUrl, initComplete = () => {}}) => {
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
            initComplete: initComplete
        });
    };

    // Initialize DataTables
    [
        {selector: '#table-groups', url: permissionManagamentSettings.url.api.getGroups},
        {selector: '#table-states', url: permissionManagamentSettings.url.api.getStates},
    ].forEach(({selector, url}) => _createDataTable({
        selector: selector,
        ajaxUrl: url,
        initComplete: () => {
            const tableApi = $(selector).DataTable();

            _initComplete(selector);
            tableApi.on('draw.dt', () => _initComplete(selector));
        }
    }));
});
