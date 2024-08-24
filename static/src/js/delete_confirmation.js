odoo.define('material_note.delete_confirmation', function (require) {
    "use strict";

    var $ = require('jquery');
    var core = require('web.core');
    var publicWidget = require('web.public.widget');

    publicWidget.registry.DeleteConfirmation = publicWidget.Widget.extend({
        selector: '#deleteModal',
        events: {
            'click .delete-button': '_onClickDeleteButton',
        },
        _onClickDeleteButton: function (event) {
            var recordId = $(event.currentTarget).data('id');
            var deleteUrl = '/material_note/delete_record/' + recordId;
            
            var form = $('#deleteForm');
            form.attr('action', deleteUrl);

            this.$el.modal('show');
        }
    });

    $(document).ready(function() {
        core.bus.trigger('delete_confirmation:init');
    });
});
