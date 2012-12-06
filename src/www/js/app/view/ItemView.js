
var ItemView = Backbone.View.extend({
    
    el: '.expose',
    
    template: _.template($('#item-template').html()),
    
    data: {},
    
    initialize: function() {
        
        _.bindAll(this, 'render');
    },
    
    render: function() {
        
        var data = {
            'pin_id': this.data.pin_id,
            'uri': this.data.uri
        }
        
        $(this.el).append(this.template(data));
        
        return this;
    }
});