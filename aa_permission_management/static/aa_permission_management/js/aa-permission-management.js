/* global DataTable, permissionManagamentSettings */

$(document).ready(() => {
    'use strict';

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
            }
        ];

        return new DataTable(selector, {
            ...permissionManagamentSettings.dataTable,
            ajax: ajaxUrl,
            columnDefs,
            order: [[0, 'asc']],
        });
    };

    // Initialize DataTables
    [
        {selector: '#table-groups', url: permissionManagamentSettings.url.api.getGroups},
        {selector: '#table-states', url: permissionManagamentSettings.url.api.getStates},
    ].forEach(({selector, url}) => createDataTable(selector, url));
});
