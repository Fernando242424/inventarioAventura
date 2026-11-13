// Activa DataTables en toda tabla con la clase "datatable".
// - Paginación, búsqueda en tiempo real y ordenamiento por columna.
// - Las columnas con la clase "no-orden" (botones de acciones) no se ordenan ni se buscan.
$(document).ready(function () {
    $('table.datatable').DataTable({
        pageLength: 10,
        columnDefs: [{ targets: 'no-orden', orderable: false, searchable: false }],
        language: {
            search: 'Buscar:',
            lengthMenu: 'Mostrar _MENU_ registros',
            info: 'Mostrando _START_ a _END_ de _TOTAL_ registros',
            infoEmpty: 'Sin registros',
            infoFiltered: '(filtrado de _MAX_ en total)',
            zeroRecords: 'No se encontraron resultados',
            emptyTable: 'No hay datos disponibles',
            paginate: { first: 'Primero', last: 'Último', next: 'Siguiente', previous: 'Anterior' }
        }
    });
});
